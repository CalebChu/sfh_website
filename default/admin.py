from django.contrib import admin
from .models import GalleryImage

# Register your models here.
@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ["id", "caption"]