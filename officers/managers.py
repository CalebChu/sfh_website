from django.db import models
import random
import string


class OfficerCodeManager(models.Manager):
    def create_code(self):
        code_value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        code = self.create(code=code_value)

        return code

    def all_officer_codes_to_list(self):
        officer_codes_list = []
        for oc in self.all():
            officer_codes_list.append(oc.to_json())

        return officer_codes_list

    def validate(self, code):
        if (self.filter(code=code).exists()):
            if (self.get(code=code).active):
                return self.get(code=code)
                
        return None
    

class OfficerManager(models.Manager):
    def is_officer(self, user):
        if self.filter(user=user).exists():
            return True
        return False