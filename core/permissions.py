from django.contrib.auth.models import User

from core.models import Manager, PersonalAdvisor, YoungPerson


def is_personal_advisor(user: User) -> bool:
    """check if the user is personal advisor"""
    if user.is_authenticated:
        return PersonalAdvisor.objects.filter(user=user).exists()
    return False


def is_young_person(user: User) -> bool:
    """check if the user is personal advisor"""
    if user.is_authenticated:
        return YoungPerson.objects.filter(user=user).exists()
    return False


def is_manager(user: User) -> bool:
    """check if the user is personal advisor"""
    if user.is_authenticated:
        return Manager.objects.filter(user=user).exists()
    return False
