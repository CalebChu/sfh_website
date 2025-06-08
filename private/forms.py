from .models import VolunteeringOpp, Event, Announcement, PointTransaction
from django import forms

class VolunteeringOppCreationForm(forms.ModelForm):
    template_name = 'opp_form_renderer.html'

    duration_field_h = forms.IntegerField(label="h")
    duration_field_m = forms.IntegerField(label="m")

    field_order = ['title', 'location', 'description', 'date_time', 'duration_field_h', 'duration_field_m']

    class Meta:
        model = VolunteeringOpp
        fields = '__all__'
        exclude = ['posted_by', 'listed', 'sign_up_open', 'members', 'complete', 'duration']
        widgets = {"location": forms.TextInput(attrs={"placeholder": "location"}), "title": forms.TextInput(attrs={"placeholder": "title"}), "description": forms.TextInput(attrs={"placeholder": "description"})}


class EventCreationForm(forms.ModelForm):
    template_name = 'opp_form_renderer.html'

    duration_field_h = forms.IntegerField(label="h")
    duration_field_m = forms.IntegerField(label="m")

    field_order = ['title', 'location', 'description', 'date_time', 'duration_field_h', 'duration_field_m']

    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['posted_by', 'listed', 'sign_up_open', 'members', 'complete', 'duration', 'attendance_open', 'last_opened_time', 'current_code', 'members_attended', 'attendance_duration']
        widgets = {"location": forms.TextInput(attrs={"placeholder": "location"}), "title": forms.TextInput(attrs={"placeholder": "title"}), "description": forms.TextInput(attrs={"placeholder": "description"})}


class AnnouncementForm(forms.ModelForm):
    template_name = 'announcements_form.html'
    content = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "post an announcement", "class": "announcement-content"}), label='')

    class Meta:
        model = Announcement
        fields = ["content"]


class PointTransactionForm(forms.ModelForm):
    class Meta:
        model = PointTransaction
        fields = ["value", "description"]