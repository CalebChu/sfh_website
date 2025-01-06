from django.shortcuts import render, redirect
from officers.models import Officer
from members.models import Member
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse, HttpResponseNotFound
from .models import VolunteeringOpp, Event, Announcement, Attendance, PointTransaction, EventAttendance
from .forms import VolunteeringOppCreationForm, EventCreationForm, AnnouncementForm, PointTransactionForm
from django.utils import timezone
from datetime import date, time, timedelta
import json
from django.db.models import Q


def check_permission(user, signed_in=True, is_member_or_officer=True, is_officer=False, is_member=False):
    """
    Checks if a user has the required permissions based on their authentication status and roles.
    Args:
        user (User): The user object to check permissions for.
        signed_in (bool, optional): Whether the user needs to be signed in. Defaults to True.
        is_member_or_officer (bool, optional): Whether the user needs to be either a member or an officer. Defaults to True.
        is_officer (bool, optional): Whether the user needs to be an officer. Defaults to False.
        is_member (bool, optional): Whether the user needs to be a member. Defaults to False.
    Returns:
        bool: True if the user has the required permissions, False otherwise.
    """
    if signed_in and not user.is_authenticated:
        return False
    if is_officer and not Officer.objects.is_officer(user):
        return False 
    if is_member and not Member.objects.member_exists(user):
        return False
    if is_member_or_officer and not (Officer.objects.is_officer(user) or Member.objects.member_exists(user)):
        return False 

    return True


def get_officer_or_member(request):
    """
    Retrieve either a Member or an Officer object based on the user in the request.

    Args:
        request (HttpRequest): The HTTP request object containing the user information.

    Returns:
        tuple: A tuple containing the retrieved object (Member or Officer) and a boolean.
               The boolean is False if the object is a Member, and True if the object is an Officer.
    """
    if Member.objects.member_exists(request.user):
        return Member.objects.get(user=request.user), False
    else:
        return Officer.objects.get(user=request.user), True


def get_dashboard_preview(model):
    """
    Generates a preview of the dashboard data and calculates overflow.
    Args:
        model: A Django QuerySet or similar iterable containing the data to be previewed.
    Returns:
        tuple: A tuple containing:
            - preview (QuerySet or list): The first two items of the model if there is overflow, 
              otherwise the entire model.
            - overflow (int): The number of items exceeding the preview limit if the model 
              contains 4 or more items, otherwise 0.
    """
    overflow = max(model.count() - 2, 0) if model.count() >= 4 else 0
    preview = model[:2] if overflow >= 2 else model

    return preview, overflow


# Create your views here.
def dashboard(request):
    """
    Renders the dashboard view for the user.
    This view checks if the user has the necessary permissions to access the dashboard.
    It retrieves the user's account and determines if the user is an officer or a member.
    Based on the user's role, it fetches the relevant volunteering opportunities and events
    that are not yet complete. The view also updates the status of volunteering opportunities
    and events.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered dashboard page with the context containing:
            - volunteering (QuerySet): The volunteering opportunities for the user.
            - v_overflow (bool): Indicator if there are more volunteering opportunities than displayed.
            - events (QuerySet): The events that are not yet complete.
            - e_overflow (bool): Indicator if there are more events than displayed.
    """
    if not check_permission(request.user):
        return HttpResponseForbidden()

    account, is_officer = get_officer_or_member(request)
    volunteering = None
    events = Event.objects.filter(complete=False)
    # announcements = Announcement.objects.all()

    VolunteeringOpp.objects.update_status()
    Event.objects.update_status()
    if is_officer:
        volunteering = VolunteeringOpp.objects.filter(posted_by=account, complete=False)
    else: 
        volunteering = VolunteeringOpp.objects.filter(members=account, complete=False)

    volunteering, v_overflow = get_dashboard_preview(volunteering)
    events, e_overflow = get_dashboard_preview(events)
    # announcements, a_overflow = get_dashboard_preview(announcements)

    return render(request, 'dashboard.html', {"volunteering": volunteering, "v_overflow": v_overflow, "events": events, "e_overflow": e_overflow})


def sign_up(request, opp_or_event):
    """
    Handles the sign-up process for an opportunity or event.
    Args:
        request (HttpRequest): The HTTP request object containing user and body data.
        opp_or_event (Model): The model class representing the opportunity or event.
    Returns:
        JsonResponse: A JSON response with the status of the sign-up process.
    Possible status values:
        - "failed": If the opportunity or event does not exist or the user does not have permission.
        - "unregistered": If the user was previously registered and has been unregistered.
        - "sign up closed": If the sign-up period is closed or the event is complete.
        - "registered": If the user has been successfully registered.
    """
    if not check_permission(request.user, is_member=True):
        return HttpResponseForbidden()

    body_unicode = request.body.decode('utf-8')
    id = int(json.loads(body_unicode))
    status = "failed"

    if opp_or_event.objects.filter(id=id).exists():
        opp = opp_or_event.objects.get(id=id)
        account, is_officer = get_officer_or_member(request)

        if not is_officer: 
            if opp in opp_or_event.objects.filter(members=account):
                opp.members.remove(account)
                status = "unregistered"
            elif not opp.sign_up_open or opp.complete:
                status = "sign up closed"
            elif not opp in opp_or_event.objects.filter(members=account):
                opp.members.add(account)

                status = "registered"

            opp.sign_up_open = opp.members.all().count() < opp.max_members
            opp.save()

    response = {"status": status}

    return JsonResponse(response)


def volunteering_opps(request):
    """
    Handle the volunteering opportunities view.
    This view handles the display and sign-up for volunteering opportunities.
    It performs the following actions:
    - Checks if the user has the necessary permissions.
    - Updates the status of volunteering opportunities.
    - Handles the sign-up process if the request method is POST.
    - Filters and processes the list of volunteering opportunities.
    - Renders the volunteering opportunities page.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The HTTP response object with the rendered volunteering opportunities page or a forbidden response.
    """
    if not check_permission(request.user):
        return HttpResponseForbidden()

    VolunteeringOpp.objects.update_status()

    if request.method == "POST":
        return sign_up(request, VolunteeringOpp)

    opps_list = VolunteeringOpp.objects.filter(listed=True)

    for opp in opps_list.filter(complete=True):
        if Attendance.objects.filter(opp=opp, marked=True).count() == opp.members.count():
            opp.listed = False
            opp.save()

    account, is_officer = get_officer_or_member(request)
    opps_list = VolunteeringOpp.objects.filter(listed=True)

    return render(request, 'volunteering_opps.html', {'opps': opps_list, 'account': account})


def volunteering_completed(request):
    """
    Handles the request to view completed volunteering opportunities.
    This view checks if the user has the necessary permissions to access the page.
    If the user does not have permission, it returns an HttpResponseForbidden.
    Otherwise, it retrieves a list of volunteering opportunities that are marked as not listed
    and renders them in the 'volunteering_opps.html' template with a context indicating
    that these opportunities are completed.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered 'volunteering_opps.html' template with the list of completed
                      volunteering opportunities, or an HttpResponseForbidden if the user lacks permission.
    """
    if not check_permission(request.user):
        return HttpResponseForbidden()

    opps_list = VolunteeringOpp.objects.filter(listed=False)

    return render(request, 'volunteering_opps.html', {'opps': opps_list, 'completed': True})


def edit_volunteering_opp(request, id):
    if not check_permission(request.user, is_officer=True):
        return HttpResponseForbidden()

    instance = VolunteeringOpp.objects.get(id=id)

    if instance.posted_by != Officer.objects.get(user=request.user):
        return HttpResponseForbidden()

    return create_volunteering_opp(request, instance=instance)


def delete_volunteering_opp(request, id):
    if not check_permission(request.user, is_officer=True):
        return HttpResponseForbidden()

    instance = VolunteeringOpp.objects.get(id=id)

    if instance.posted_by != Officer.objects.get(user=request.user):
        return HttpResponseForbidden()

    instance.delete()

    return redirect("private:volunteering_opps")


def handle_form(request, form_type, model, instance=None):
    posted_by = Officer.objects.get(user=request.user)
    form = form_type(request.POST, instance=model(posted_by=posted_by))

    if instance:
        form = form_type(request.POST, instance=instance)

    if form.is_valid():
        form.instance.duration = timedelta(hours=form.cleaned_data["duration_field_h"], minutes=form.cleaned_data["duration_field_m"])

        form.save()

        return True

    return False


def create_volunteering_opp(request, instance=None):
    if not check_permission(request.user, is_officer=True):
        return HttpResponseForbidden()

    if request.method == "POST":
        if handle_form(request, VolunteeringOppCreationForm, VolunteeringOpp, instance=instance):
            return redirect("private:volunteering_opps")

    form = VolunteeringOppCreationForm()
    if (instance):
        form = VolunteeringOppCreationForm(instance=instance)

    return render(request, 'create_volunteering_opp.html', {'form': form, 'title': 'Volunteering'})


def volunteering_attendance(request, id):
    if not check_permission(request.user, is_officer=True):
        return HttpResponseForbidden()

    volunteering = VolunteeringOpp.objects.get_if_exists(id)
    if volunteering.posted_by != Officer.objects.get(user=request.user):
        return HttpResponseForbidden()

    if request.method == "POST":
        status = "incomplete"
        body_unicode = request.body.decode('utf-8')
        fetch_body = json.loads(body_unicode)
        member_id = None

        try:
            member_id = int(fetch_body["id"])
        except ValueError:
            status = "ValueError"
            
        action = fetch_body["action"]

        if member_id and Member.objects.filter(id=member_id, volunteeringopp__id=id).exists():
            member = Member.objects.get(id=member_id)
            attendance_obj = Attendance.objects.get(member=member, opp_id=id)

            if action == "present" or action == "absent":
                VOLUNTEERING_POINT_VALUE = 10
                if not attendance_obj.point_transaction:
                    attendance_obj.point_transaction = PointTransaction(performed_by=Officer.objects.get(user=request.user), for_volunteering=True)

                attendance_obj.attended = action == "present"
                status = action

                attendance_obj.point_transaction.member = member
                attendance_obj.point_transaction.date_time = timezone.now()
                attendance_obj.point_transaction.subtract = action == "absent"
                attendance_obj.point_transaction.value = VOLUNTEERING_POINT_VALUE
                attendance_obj.point_transaction.description = attendance_obj.opp.title
                attendance_obj.point_transaction.value *= -1 if attendance_obj.point_transaction.subtract else 1

                attendance_obj.point_transaction.save()
            
                attendance_obj.marked = True
                attendance_obj.save()


        response = {"status": status}

        return JsonResponse(response)

    attendees_unmarked = Attendance.objects.filter(opp_id=id, marked=False)
    attendees_present = Attendance.objects.filter(opp_id=id, attended=True, marked=True)
    attendees_absent = Attendance.objects.filter(opp_id=id, attended=False, marked=True)

    return render(request, 'volunteering_attendance.html', {'attendees': attendees_unmarked, 'present': attendees_present, 'absent': attendees_absent})


def events(request):
    if not check_permission(request.user):
        return HttpResponseForbidden() 

    Event.objects.update_status()
    eventObjs = Event.objects.filter(listed=True)

    return render(request, 'events.html', {'events': eventObjs})


def events_completed(request):
    if not check_permission(request.user):
        return HttpResponseForbidden() 

    eventObjs = Event.objects.filter(listed=False)

    return render(request, 'events.html', {'events': eventObjs, 'completed': True})


def generate_event_attendance(request, id, option=None):
    if not check_permission(request.user, is_officer=True):
        return HttpResponseForbidden()

    event = Event.objects.get_if_exists(id)

    if event:
        if option:
            if option == "refresh" or option == "reopen":
                event.last_opened_time = timezone.now()
                event.attendance_open = True

                if option == "refresh":
                    event.current_code = Event.objects.generate_code()

            if option == "close" or option == "markabsences":
                event.attendance_open = False

                if option == "markabsences":
                    event.listed = False
                    for member in Member.objects.filter(~Q(event=event)):
                        attendance_obj = EventAttendance.objects.create(event=event, member=member)
                        attendance_obj.point_transaction = PointTransaction.objects.create(performed_by=event.posted_by, for_event=True, member=member, value=-1*event.points_available, description=event.title, subtract=True)
                        attendance_obj.save()

            event.save()

            return redirect("private:event_attendance", id=id)

        if event and event.attendance_open:
            if timezone.now() > event.last_opened_time + event.attendance_duration:
                event.attendance_open = False
                event.save()

        if not event.attendance_open and event.current_code == None:
            event.current_code = Event.objects.generate_code()
            event.attendance_open = True
            event.last_opened_time = timezone.now()

            event.save()

        return render(request, "event_attendance.html", {"event": event})

    return HttpResponseNotFound()


def create_event(request, instance=None):
    if not check_permission(request.user, is_officer=True):
        return HttpResponseForbidden()

    if request.method == "POST":
        if handle_form(request, EventCreationForm, Event, instance=instance):
            return redirect("private:events")

    form = EventCreationForm()
    if (instance):
        form = EventCreationForm(instance=instance)

    return render(request, 'create_volunteering_opp.html', {'form': form, 'title': 'Event'})


def edit_event(request, id):
    """
    Handles the editing of an existing event.
    This view checks if the user has the necessary permissions to edit an event.
    If the user does not have the required permissions, it returns an HTTP 403 Forbidden response.
    If the user has the required permissions, it retrieves the event instance by its ID and
    delegates the request to the create_event view for further processing.
    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the event to be edited.
    Returns:
        HttpResponse: The response generated by the create_event view or an HTTP 403 Forbidden response.
    """
    if not check_permission(request.user, is_officer=True):
        return HttpResponseForbidden()

    instance = Event.objects.get(id=id)

    return create_event(request, instance=instance)    


def event_attendance(request, eid, code):
    """
    Handles the attendance of an event by a user.
    This view function checks if the user has the necessary permissions to attend the event.
    If the user is permitted, it validates the attendance code and updates the event attendance
    records accordingly. It also creates a point transaction for the attended event.
    Args:
        request (HttpRequest): The HTTP request object containing user information.
        eid (int): The ID of the event.
        code (str): The attendance code provided by the user.
    Returns:
        HttpResponse: Renders the event attendance result page with the validation result.
    """
    if not check_permission(request.user):
        return HttpResponseForbidden()

    valid, result = validate_attendance(eid, request.user, code)

    print(valid, result)

    if valid:
        event = Event.objects.get(id=eid)
        member = Member.objects.get(user=request.user)
        event.members_attended.add(member)

        attendance_obj = EventAttendance.objects.get(event_id=eid, member=member)
        attendance_obj.attended = True
        attendance_obj.point_transaction = PointTransaction.objects.create(performed_by=event.posted_by, for_event=True, member=member, value=event.points_available, description=event.title)
        attendance_obj.save()

        return render(request, "event_attendance_result.html", {"result": result})
    else:
        return render(request, "event_attendance_result.html", {"result": result})


def validate_attendance(eid, user, code):
    """
    Validates the attendance of a user for a specific event.
    Args:
        eid (int): The ID of the event.
        user (User): The user object representing the attendee.
        code (str): The attendance code provided by the user.
    Returns:
        tuple: A tuple containing a boolean and an integer.
            - The boolean indicates whether the attendance is valid.
            - The integer is an error code representing the reason for invalid attendance:
                1. The user is not a member.
                2. The event does not exist.
                3. The provided code does not match the event's current code.
                4. The user has already attended the event.
                5. The attendance period for the event is closed.
                0. The attendance is valid.
    """
    event = Event.objects.get_if_exists(eid)

    if event and event.attendance_open:
        if timezone.now() > event.last_opened_time + event.attendance_duration:
            event.attendance_open = False
            event.save()

    if not Member.objects.member_exists(user):
        return False, 1
    if not event:
        return False, 2
    if not (event.current_code == code):
        return False, 3
    if Member.objects.get(user=user) in event.members_attended.all():
        return False, 4
    if not event.attendance_open:
        return False, 5
    return True, 0


def announcements(request):
    if not check_permission(request.user):
        return HttpResponseForbidden()

    if request.method == "POST":
        if not check_permission(request.user, is_officer=True):
            return HttpResponseForbidden()

        officer = Officer.objects.get(user=request.user)
        form = AnnouncementForm(request.POST, instance=Announcement(posted_by=officer))

        if form.is_valid():
            form.save()
        
        return redirect("private:announcements")

    announcementsDisplay = Announcement.objects.all()
    form = AnnouncementForm

    return render(request, 'announcements.html', {'announcements': announcementsDisplay, "form": form})


def points(request): 
    if not check_permission(request.user):
        return HttpResponseForbidden()

    account, is_officer = get_officer_or_member(request)    

    if (account and not is_officer):
        history = PointTransaction.objects.filter(member=account)

        return render(request, 'points.html', {"points": count_points(history), "history": history})

    return render(request, 'points.html', {"members": Member.objects.all()})


def count_points(transactions):
    return sum(transactions.values_list('value', flat=True))


def edit_points(request, ids):
    if not check_permission(request.user, is_officer=True):
        return HttpResponseForbidden()

    members_list = [Member.objects.get(id=int(id)) for id in set(ids.split("+"))]

    if request.method == "POST":
        officer = Officer.objects.get(user=request.user)

        for member in members_list:
            point_transaction = PointTransactionForm(request.POST, instance=PointTransaction(member=member, performed_by=officer))
            point_transaction.save()

            if point_transaction.instance.value < 0:
                point_transaction = PointTransaction.objects.get(id=point_transaction.instance.id)
                point_transaction.subtract = True
                point_transaction.save()
            
        return redirect("private:points")

    return render(request, 'point_transaction.html', {"members": members_list, "form": PointTransactionForm})


def leaderboard(request):
    if not check_permission(request.user):
        return HttpResponseForbidden()

    users_unsorted = Member.objects.all()
    users_sorted = sorted(users_unsorted, key=lambda t: -1*count_points(PointTransaction.objects.filter(member=t)))

    return render(request, "leaderboard.html", {"leaderboard": users_sorted})
