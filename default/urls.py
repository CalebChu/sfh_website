from django.urls import path
from . import views

app_name = 'default'

urlpatterns = [
    path('', views.index, name='index'),
    path('gallery', views.gallery, name='gallery'),
    path('upload_gallery_image', views.upload_gallery_image, name='upload_gallery_image'),
    path('officers_info', views.officers_info, name='officers_info'),
    path('site_credits', views.site_credits, name='site_credits'),

    path('sign-in', views.sign_in, name='sign_in'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
]