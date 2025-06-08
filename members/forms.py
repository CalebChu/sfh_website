from django import forms
from django.forms import ModelForm
from .models import Member
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Member


# class MemberCreationForm(UserCreationForm):

#     class Meta:
#         model = Member
#         fields = ("email",)


# class MemberChangeForm(UserChangeForm):

#     class Meta:
#         model = Member
#         fields = ("email",)


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ["grade", "phone_number"]

