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


def check_permission(user, signed_in=True, is_member_or_officer=True, is_officer=False):
    if signed_in and not user.is_authenticated:
        return False
    if is_officer and not Officer.objects.is_officer(user):
        return False 
    if is_member_or_officer and not (Officer.objects.is_officer(user) or Member.objects.member_exists(user)):
        return False 

    return True


def get_officer_or_member(request):
    if Member.objects.member_exists(request.user):
        return Member.objects.get(user=request.user), False
    else:
        return Officer.objects.get(user=request.user), True


def get_dashboard_preview(model):
    overflow = max(model.count() - 2, 0) if model.count() >= 4 else 0
    preview = model[:2] if overflow >= 2 else model

    return preview, overflow


# Create your views here.
def dashboard(request):
    if not check_permission(request.user):
        return HttpResponseForbidden()

    account, is_officer = get_officer_or_member(request)
    volunteering = None
    events = Event.objects.all()
    announcements = Announcement.objects.all()

    VolunteeringOpp.objects.update_status()
    Event.objects.update_status()
    if is_officer:
        volunteering = VolunteeringOpp.objects.filter(posted_by=account, listed=True)
    else: 
        volunteering = VolunteeringOpp.objects.filter(members=account, listed=True)

    volunteering, v_overflow = get_dashboard_preview(volunteering)
    events, e_overflow = get_dashboard_preview(events)
    announcements, a_overflow = get_dashboard_preview(announcements)

    return render(request, 'dashboard.html', {"volunteering": volunteering, "v_overflow": v_overflow, "events": events, "e_overflow": e_overflow, "announcements": announcements, "a_overflow": a_overflow,})


def sign_up(request, opp_or_event):
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
    if not check_permission(request.user):
        return HttpResponseForbidden()

    VolunteeringOpp.objects.update_status()

    if request.method == "POST":
        return sign_up(request, VolunteeringOpp)

    opps_list = VolunteeringOpp.objects.filter(listed=True)
    account, is_officer = get_officer_or_member(request)

    return render(request, 'volunteering_opps.html', {'opps': opps_list, 'account': account})


def edit_volunteering_opp(request, id):
    instance = VolunteeringOpp.objects.get(id=id)

    if instance.posted_by != Officer.objects.get(user=request.user):
        return HttpResponseForbidden()

    return create_volunteering_opp(request, instance=instance)


def delete_volunteering_opp(request, id):
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


def generate_event_attendance(request, id, option=None):
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
    instance = Event.objects.get(id=id)

    if instance.posted_by != Officer.objects.get(user=request.user):
        return HttpResponseForbidden()

    return create_event(request, instance=instance)    


def event_attendance(request, eid, code):
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
    if request.method == "POST":
        officer = Officer.objects.get(user=request.user)
        form = AnnouncementForm(request.POST, instance=Announcement(posted_by=officer))

        if form.is_valid():
            form.save()
        
        return redirect("private:announcements")

    announcementsDisplay = Announcement.objects.all()
    form = AnnouncementForm

    return render(request, 'announcements.html', {'announcements': announcementsDisplay, "form": form})


def points(request):
    account, is_officer = get_officer_or_member(request)    

    if (account and not is_officer):
        history = PointTransaction.objects.filter(member=account)

        return render(request, 'points.html', {"points": count_points(history), "history": history})

    return render(request, 'points.html', {"members": Member.objects.all()})


def count_points(transactions):
    return sum(transactions.values_list('value', flat=True))


def edit_points(request, ids):
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
    users_unsorted = Member.objects.all()
    users_sorted = sorted(users_unsorted, key=lambda t: -1*count_points(PointTransaction.objects.filter(member=t)))

    return render(request, "leaderboard.html", {"leaderboard": users_sorted})
