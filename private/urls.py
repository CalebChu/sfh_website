from django.urls import path, re_path
from . import views

app_name = 'private'

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('create_opp', views.create_volunteering_opp, name='create_opp'),
    path('edit_opp/<int:id>', views.edit_volunteering_opp, name='edit_opp'),
    path('delete_opp/<int:id>', views.delete_volunteering_opp, name='delete_opp'),
    path('volunteering', views.volunteering_opps, name='volunteering_opps'),
    path('volunteering/completed', views.volunteering_completed, name='volunteering_completed'),
    path('events', views.events, name='events'),
    path('events/completed', views.events_completed, name='events_completed'),
    re_path(r'^event_attendance/(?P<id>[0-9]+)/(?:(?P<option>[a-z]+)/)?$', views.generate_event_attendance, name='event_attendance'),
    path('event_attendance_confirmation/<int:eid>+<str:code>', views.event_attendance, name='event_attendance_confirmation'),
    path('create_event', views.create_event, name='create_event'),
    path('edit_event/<int:id>', views.edit_event, name='edit_event'),
    path('announcements', views.announcements, name='announcements'),
    path('v_attendance/<int:id>', views.volunteering_attendance, name="v_attendance"),
    path('points', views.points, name='points'),
    path('leaderboard', views.leaderboard, name='leaderboard'),
    re_path(r'^edit_points/(?P<ids>([0-9]+\+?)+)$', views.edit_points, name='edit_points'),
]
