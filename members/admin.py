from .models import Member
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# from .forms import MemberCreationForm, MemberChangeForm
from .models import Member

# Register your models here.

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["member_name", "grade"]

    @admin.display(empty_value="-")
    def member_name(self, obj):
        user = obj.user
        return f"{user.first_name} {user.last_name}"

# class Admin(UserAdmin):
#     add_form = MemberCreationForm
#     form = MemberChangeForm
#     model = Member
#     list_display = ("email", "is_staff", "is_active",)
#     list_filter = ("email", "is_staff", "is_active",)
#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
#     )
#     add_fieldsets = (
#         (None, {
#             "classes": ("wide",),
#             "fields": (
#                 "email", "password1", "password2", "is_staff",
#                 "is_active", "groups", "user_permissions"
#             )}
#         ),
#     )
#     search_fields = ("email",)
#     ordering = ("email",)

# admin.site.register(Member, Admin)