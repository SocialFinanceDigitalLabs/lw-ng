from functools import reduce

from django import template

from lw_common.constants import colours

register = template.Library()


def usercolour(user):
    hash = reduce(lambda x, y: x + ord(y), user.username, 0)
    return colours[hash % len(colours)]


register.filter('usercolour', usercolour)
