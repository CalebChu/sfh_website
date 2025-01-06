from django import forms
from .models import GalleryImage
from django.contrib.auth.models import User


class GalleryImageForm(forms.ModelForm):
    template_name = "form_renderer.html"

    class Meta:
        model = GalleryImage
        fields = "__all__"
        widgets = {"caption": forms.TextInput(attrs={"placeholder": "caption"})}


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
