from django.db import models

class MemberManager(models.Manager):
    def member_exists(self, user):
        return self.filter(user=user).exists()