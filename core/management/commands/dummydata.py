import os
from django.apps import apps
from django.core.management.base import BaseCommand

from core.models import PersonalAdvisor, YoungPerson
from django.contrib.auth import get_user_model
User = get_user_model()

class Command(BaseCommand):
    help = "Deletes all data in user defined models"
    def handle(self, *args, **options):
        pa = self.create_pa("Peter","Anders")
        for i in range(10):
            self.create_yp("Young",f"Person{i}",pa)


    def create_pa(self, firstname, lastname):
        user, created = User.objects.update_or_create(username = f"{firstname}.{lastname}", defaults = dict(first_name = firstname, last_name = lastname))
        pa, created = PersonalAdvisor.objects.update_or_create(user = user, defaults = dict(is_manager = True))
        user.set_password("password")
        user.is_staff = True
        user.save()
        return pa

    def create_yp(self, firstname, lastname, pa):
        user, created = User.objects.update_or_create(username = f"{firstname}.{lastname}", defaults = dict(first_name = firstname, last_name = lastname))
        yp, created = YoungPerson.objects.update_or_create(user = user)
        yp.personal_advisors.add(pa)
        return yp