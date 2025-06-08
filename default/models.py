from django.db import models

# Create your models here.
class GalleryImage(models.Model):
    image = models.ImageField(upload_to='default/files/gallery')
    caption = models.CharField(max_length=200, blank=True)
    auto_scale = models.BooleanField(default=False)
    