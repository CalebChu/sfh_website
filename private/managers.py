from django.db import models
from django.utils import timezone
from random import randrange, choice

class BaseListingManager(models.Manager):
    def update_status(self):
        for listing in self.filter(listed=True):
            if timezone.now() > listing.date_time + listing.duration:
                listing.complete = True
                listing.save()


    def get_if_exists(self, id):
        if self.filter(id=id).exists():
            return self.get(id=id)
        else:
            return None

    
    def generate_code(self):
        code = ""

        upper = [chr(val) for val in range(ord('A'), ord('Z')+1)]
        lower = [chr(val) for val in range(ord('a'), ord('z')+1)]
        nums = [chr(val) for val in range(ord('0'), ord('9')+1)]

        choices = [upper, lower, nums]

        for ch in range(8):
            selection = randrange(0, 3)

            code += choice(choices[selection])

        return code