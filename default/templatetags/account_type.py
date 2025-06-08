from django import template

register = template.Library() 


@register.filter(name='is_officer') 
def is_officer(user):
    return user.groups.filter(name='Officers').exists() 


@register.filter(name='is_member') 
def is_member(user):
    return user.groups.filter(name='Members').exists() 