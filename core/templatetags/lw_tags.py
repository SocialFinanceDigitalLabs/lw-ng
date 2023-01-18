from django import template

from core import permissions

register = template.Library()

register.filter("is_personal_advisor", permissions.is_personal_advisor)
register.filter("is_young_person", permissions.is_young_person)
register.filter("is_manager", permissions.is_manager)
