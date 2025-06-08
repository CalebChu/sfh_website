from django.db import models
from django.utils.translation import gettext_lazy as _
from officers.models import Officer
from members.models import Member
from django.utils import timezone
from .managers import BaseListingManager
from datetime import timedelta


# Create your models here.
class BaseListing(models.Model):
    posted_by = models.ForeignKey(Officer, on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=100)

    date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    duration = models.DurationField()
    
    location = models.TextField(_("Address or location"))

    description = models.TextField(_("description or extra info"))

    show_officer_info = models.BooleanField(default=True)

    listed = models.BooleanField(default=True)
    complete = models.BooleanField(default=False)

    points_available = models.IntegerField(default=10)

    objects = BaseListingManager()

    def compare_time(self):
        future = self.date > timezone.now() and self.start_time > timezone.now()

        return {"in_the_future": future}

    def duration_hours(self):
        secToHours = 60**2

        if not self.duration:
            return 0

        return int(self.duration.seconds/secToHours)

    def duration_minutes(self):
        secToMinutes = 60
        remainderMinutes = 60

        if not self.duration:
            return 0

        return int((self.duration.seconds/secToMinutes)%remainderMinutes)

    class Meta:
        ordering = ['date_time', 'title']
        abstract = True


class VolunteeringOpp(BaseListing):
    members = models.ManyToManyField(Member, through="Attendance")
    max_members = models.PositiveIntegerField(default=0)
    sign_up_open = models.BooleanField(default=True)


class Event(BaseListing):
    points_available = models.IntegerField(default=10)

    members_attended = models.ManyToManyField(Member, through="EventAttendance")
    attendance_open = models.BooleanField(default=False)
    last_opened_time = models.DateTimeField(null=True)
    current_code = models.CharField(max_length=8, null=True)
    attendance_duration = models.DurationField(default=timedelta(minutes=10))

    def attendance_duration_minutes(self):
        secToMinutes = 60
        remainderMinutes = 60

        if not self.attendance_duration:
            return 0

        return int((self.attendance_duration.seconds/secToMinutes)%remainderMinutes)

class PointTransaction(models.Model):
    performed_by = models.ForeignKey(Officer, on_delete=models.SET_NULL, null=True)

    value = models.IntegerField()
    subtract = models.BooleanField(default=False)

    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)

    date_time = models.DateTimeField(default=timezone.now)

    for_event = models.BooleanField(default=False)
    for_volunteering = models.BooleanField(default=False)

    description = models.CharField(max_length=100)

    class Meta:
        ordering = ['-date_time']


class BaseAttendance(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    point_transaction = models.OneToOneField(PointTransaction, on_delete=models.CASCADE, null=True)

    attended = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Attendance(BaseAttendance):
    opp = models.ForeignKey(VolunteeringOpp, on_delete=models.CASCADE)
    marked = models.BooleanField(default=False)

    class Meta:
        ordering = ['-opp__date_time', 'opp__title']


class EventAttendance(BaseAttendance):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-event__date_time', 'event__title']


class Announcement(models.Model):
    posted_by = models.ForeignKey(Officer, on_delete=models.CASCADE, null=True)

    date_posted = models.DateTimeField(default=timezone.now)

    content = models.TextField()

    class Meta:
        ordering = ['-date_posted']
