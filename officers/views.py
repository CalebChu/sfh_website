from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, JsonResponse, HttpResponseForbidden, HttpResponse

from private.models import Attendance, PointTransaction
from .models import OfficerCode, Officer
from members.models import Member
from .forms import CodeForm, OfficerForm
from django.contrib.auth.models import Group
from default.forms import UserForm
from django.conf import settings


def check_permission(user, signed_in=True, is_officer=True, super_user=False):
    if signed_in and not user.is_authenticated:
        return False
    if is_officer and not Officer.objects.filter(user=user).exists():
        return False
    if super_user and not user.is_superuser:
        return False

    return True


def handle_form_post(request):
    code_form = CodeForm(request.POST)

    if code_form.is_valid():
        code_object = OfficerCode.objects.validate(code_form.cleaned_data["code"])

        if code_object:
            officer, created = Officer.objects.get_or_create(user=request.user)

            officers_group, c = Group.objects.get_or_create(name='Officers')

            form = OfficerForm(request.POST, request.FILES, instance=officer)
            user_form = UserForm(request.POST, instance=request.user)

            if form.is_valid() and user_form.is_valid() and created and settings.SIGN_UPS_OPEN:
                form.save()
                user_form.save()
                request.user.groups.add(officers_group)

                code_object.use(officer)

                if Member.objects.member_exists(request.user):
                    Member.objects.get(user=request.user).delete()
                    members_group, c = Group.objects.get_or_create(name='Members')
                    request.user.groups.remove(members_group)

                return redirect('default:index')
            
    if Officer.objects.is_officer(request.user):
        Officer.objects.get(user=request.user).delete()

    return HttpResponse("Could not create officer profile.")


def officer_codes(request):
    if not check_permission(request.user, is_officer=False, super_user=True):
        return HttpResponseForbidden()

    if request.method == "POST":
        data = OfficerCode.objects.create_code().to_json()

        return JsonResponse(data)

    existing_codes_list = [code_dict for code_dict in OfficerCode.objects.all_officer_codes_to_list()]
    return render(request, "officer_codes.html", {"existing_codes": existing_codes_list})


def officer_form(request):
    if not check_permission(request.user, is_officer=False):
        return HttpResponseForbidden()

    if request.method == "POST":
        return handle_form_post(request)

    if Officer.objects.is_officer(request.user):
        return redirect("officers:edit_profile")

    form = OfficerForm()
    code_form = CodeForm()
    user_form = UserForm(instance=request.user)

    return render(request, "officer_form.html", {"code_form": code_form, "officer_form": form, "user_form": user_form})


def handle_profile_post(request, officer):
    user_form = UserForm(request.POST, instance=request.user)
    form = OfficerForm(request.POST, request.FILES, instance=officer)

    if form.is_valid() and user_form.is_valid():
        form.save()
        user_form.save()

        return None
    else:
        return HttpResponse("could not make profile edit")


def edit_profile(request):
    if not check_permission(request.user):
        return HttpResponseForbidden()

    officer = Officer.objects.get(user=request.user)

    if request.method == "POST":
        res = handle_profile_post(request, officer)

        if res:
            return res
                  
    form = OfficerForm(instance=officer)
    user_form = UserForm(instance=request.user)

    return render(request, "edit_officer_profile.html", {"officer_form": form, "user_form": user_form})


def profile(request, id):
    if not check_permission(request.user, is_officer=False):
        return HttpResponseForbidden()

    if (not Officer.objects.filter(id=id).exists()):
        return HttpResponseNotFound()
    
    officer = Officer.objects.get(id=id)
     
    return render(request, "profile.html", {"officer": officer})

