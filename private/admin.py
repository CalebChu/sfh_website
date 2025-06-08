from django.contrib import admin
from .models import VolunteeringOpp, Event, Announcement, Attendance, EventAttendance, PointTransaction

# Register your models here.
@admin.register(VolunteeringOpp)
class VolunteeringOppAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Announcement)
class EventAdmin(admin.ModelAdmin):
    list_display = ["id", "content"]


admin.site.register(Attendance)
admin.site.register(EventAttendance)
admin.site.register(PointTransaction)
# class EventAdmin(admin.ModelAdmin):
    # list_display = ["id"]