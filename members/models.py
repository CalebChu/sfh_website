from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .managers import MemberManager
from phonenumber_field.modelfields import PhoneNumberField

# from .managers import CustomUserManager

# Create your models here.
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    GRADE_CHOICES = (
        ( 9, "Freshman"),
        (10, "Sophomore"),
        (11, "Junior"),
        (12, "Senior"),
    )
    grade = models.IntegerField(choices=GRADE_CHOICES, null=True)
    phone_number = PhoneNumberField(blank=True)

    objects = MemberManager()

    def is_complete(self):
        if self.user and self.grade and self.phone_number:
            return True
        return False

    def __str__(self):
        return self.user.__str__()
