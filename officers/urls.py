from django.urls import path
from . import views

app_name = 'officers'

urlpatterns = [
    path('codes', views.officer_codes, name='codes'),
    path('form', views.officer_form, name='form'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('profile/<int:id>', views.profile, name='profile'),
]