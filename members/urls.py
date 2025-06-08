from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('form', views.form, name='form'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('profile/<int:id>', views.profile, name='profile'),
]