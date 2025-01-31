import os
import environ

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from members.models import Member
from officers.models import Officer
from .forms import GalleryImageForm
from .models import GalleryImage

env = environ.Env()
environ.Env().read_env()

def check_permission(user, signed_in=True, is_officer=True):
    if signed_in and not user.is_authenticated:
        return False
    if is_officer and not Officer.objects.filter(user=user).exists():
        return False

    return True


def is_officer(user):
    is_officer = False
    if user.is_authenticated:
        is_officer = Officer.objects.is_officer(user)

    return is_officer


def sign_in(request):
    return render(request, 'sign_in.html', {"full_url": request.build_absolute_uri('/auth-receiver')})


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), '315344692568-7ob5gte8klqm0jfiknp1stiki0173qkp.apps.googleusercontent.com'
        )
    except ValueError:
        return HttpResponse(status=403)

    request.session['user_data'] = user_data

    user, created = User.objects.get_or_create(username=user_data['email'], email=user_data['email'])

    if created:
        if 'given_name' in user_data:
            user.first_name = user_data['given_name']
        if 'family_name' in user_data:
            user.last_name = user_data['family_name']

        user.save()

    login(request, user)

    if not Member.objects.member_exists(user) and not Officer.objects.is_officer(user):
        return redirect('members:form')
    return redirect('default:index')


def sign_out(request):
    del request.session['user_data']
    logout(request)
    return redirect('default:index')


def index(request):
    return render(request, "index.html")


def gallery(request):
    return render(request, "gallery.html", {"images": GalleryImage.objects.all().order_by("-id")})


def handle_gallery_image_upload(request):
    galleryImageSubmission = GalleryImageForm(request.POST, request.FILES)

    if galleryImageSubmission.is_valid():
        galleryImageSubmission.save()

        return redirect('default:gallery')

    return HttpResponse("could not upload image")


def upload_gallery_image(request):
    if not check_permission(request.user):
        return HttpResponseForbidden()

    if request.POST:
        return handle_gallery_image_upload(request)

    return render(request, "upload_gallery_image.html", {"form": GalleryImageForm})


def officers_info(request):
    officersList = Officer.objects.all()

    return render(request, 'officers.html', {"officers": officersList})


def site_credits(request):
    return render(request, 'credit.html')
