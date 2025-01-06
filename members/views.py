from django.shortcuts import render, redirect
from .forms import MemberForm
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from .models import Member
from private.models import Attendance, EventAttendance, PointTransaction
from django.contrib.auth.models import Group
from default.forms import UserForm


def check_permission(user, signed_in=True, completed_form=True):
    if signed_in and not user.is_authenticated:
        return False
    if completed_form and not Member.objects.get(user=user).is_complete():
        return False 

    return True


def handle_form_post(request):
    member, created = Member.objects.get_or_create(user=request.user)

    members_group, c = Group.objects.get_or_create(name='Members')

    form = MemberForm(request.POST, instance=member)
    user_form = UserForm(request.POST, instance=request.user)

    if form.is_valid() and user_form.is_valid() and created:
        request.user.groups.add(members_group)
        form.save()
        user_form.save()

        return redirect("default:index")
        
    if Member.objects.member_exists(request.user):
        Member.objects.get(user=request.user).delete()

    return HttpResponse("Could not create member profile.")

# Create your views here.
def form(request):
    if not check_permission(request.user, completed_form=False):
        return HttpResponseForbidden()

    if request.method == "POST":
        return handle_form_post(request)

    if (Member.objects.member_exists(request.user)):
        return redirect('members:edit_profile') 

    user_form = UserForm(instance=request.user)
    form = MemberForm()

    return render(request, "member_form.html", {"form": form, "user_form": user_form})


def handle_profile_post(request, member):
    user_form = UserForm(request.POST, instance=request.user)
    form = MemberForm(request.POST, instance=member)

    if user_form.is_valid() and form.is_valid():
        user_form.save()
        form.save()

        return None
    else:
        return HttpResponse("could not make profile edit")


def edit_profile(request):
    if not check_permission(request.user, completed_form=False):
        return HttpResponseForbidden()

    member = Member.objects.get(user=request.user)

    if request.method == "POST":
        res = handle_profile_post(request, member)

        if res:
            return res

    user_form = UserForm(instance=request.user)
    form = MemberForm(instance=member)

    return render(request, "edit_profile.html", {"form": form, "user_form": user_form})


def profile(request, id):
    if (not Member.objects.filter(id=id).exists()):
        return HttpResponseNotFound()
    
    member = Member.objects.get(id=id)
    volunteering_attended = Attendance.objects.filter(member=member, attended=True).count()
    events_attended = EventAttendance.objects.filter(member=member, attended=True).count()
    points = count_points(PointTransaction.objects.filter(member=member))

    users_unsorted = Member.objects.all()
    users_sorted = sorted(users_unsorted, key=lambda t: -1*count_points(PointTransaction.objects.filter(member=t)))
    point_rank = users_sorted.index(member) + 1
     
    return render(request, "profile.html", {"member": member, "points": points, "v_attended": volunteering_attended, "e_attended": events_attended, "ranking": point_rank})


def count_points(transactions):
    return sum(transactions.values_list('value', flat=True))