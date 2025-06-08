from django.contrib import admin
from .models import Officer
from .models import OfficerCode

# Register your models here.
@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    list_display = ["officer_name", "role", "signed_up_with_code"]

    @admin.display(empty_value="-")
    def officer_name(self, obj):
        user = obj.user
        return f"{user.first_name} {user.last_name}"

    def signed_up_with_code(self, obj):
        code = OfficerCode.objects.get(used_by=obj)
        return code.code


@admin.register(OfficerCode)
class OfficerAdmin(admin.ModelAdmin):
    list_display = ["code", "active"]
