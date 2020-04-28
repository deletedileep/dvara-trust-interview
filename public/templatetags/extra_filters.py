from django import template
from django.db.models import Q, Count, Case, When, IntegerField, Max, Prefetch, OuterRef, Subquery, Aggregate, CharField, Value, Sum, Avg
from django.db.models.functions import Cast, Coalesce
from admin_portal.models import UserDetails
register = template.Library()

@register.filter()
def to_int(value):
    return int(value)

@register.filter
def get_type(value):
    return type(value)

@register.filter()
def field_label(value):
    value = value.replace('_', ' ')
    return value.title()

@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()

@register.filter(name='split')
def split(value, arg):
    return value.split(',')

@register.filter
def children_count(user_data):
    if hasattr(user_data, 'userdetails') and user_data.userdetails:
        result =  UserDetails.objects.filter(parent=user_data.userdetails).count()
        return result
    else:
        return 0

