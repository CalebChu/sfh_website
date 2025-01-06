from django import template
from private.models import PointTransaction

register = template.Library()

@register.filter(name='account_points')
def account_points(member):
    return sum(PointTransaction.objects.filter(member=member).values_list('value', flat=True))
