from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import OfficerCodeManager, OfficerManager
from phonenumber_field.modelfields import PhoneNumberField

# from .managers import CustomUserManager

# Create your models here.
class Officer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='officers/files/images', blank=True)
    role = models.CharField(max_length=50, blank=True, null=True)

    phone_number = PhoneNumberField(blank=True)

    objects = OfficerManager()

    def is_complete(self):
        if self.user:
            return True
        return False

    def __str__(self):
        return self.user.__str__()


class OfficerCode(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=12, unique=True)
    active = models.BooleanField(default=True)
    used_by = models.OneToOneField(Officer, on_delete=models.SET_NULL, null=True)

    objects = OfficerCodeManager()

    def to_json(self):
        used_by = self.used_by

        if used_by:
            used_by = used_by.__str__()
        else:
            used_by = "-"

        return {"id": self.id, "code": self.code, "active": str(self.active), "used_by": used_by}

    def use(self, officer):
        self.active = False
        self.used_by = officer
        self.save()
