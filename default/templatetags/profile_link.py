from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name="profile", is_safe=True)
def profile(member):
    name = member.user.first_name + " " + member.user.last_name
    uid = member.id

    format_str = f'<a class="profile-link" href="/members/profile/{uid}">{name}</a>'

    return mark_safe(format_str)


@register.filter(name="officer_profile", is_safe=True)
def officer_profile(officer):
    name = officer.user.first_name + " " + officer.user.last_name
    uid = officer.id

    format_str = f'<a class="profile-link" href="/officers/profile/{uid}">{name}</a>'

    return mark_safe(format_str)
