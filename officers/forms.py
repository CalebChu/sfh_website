from django import forms
from .models import Officer

class CodeForm(forms.Form):
    code = forms.CharField(max_length=12)
    

class OfficerForm(forms.ModelForm):
    class Meta:
        model = Officer
        fields = "__all__"
        exclude = ["user"]