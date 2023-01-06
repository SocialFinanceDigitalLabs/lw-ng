from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import factory
from core.factories.people import ManagerFactory

from core.models import PersonalAdvisor, YoungPerson, Manager, Goal, Action

User = get_user_model()


class Command(BaseCommand):
    help = "Deletes all data in user defined models"

    def add_arguments(self, parser):
        parser.add_argument("number_of_managers", type=int, default=100)

    def handle(self, *args, **options):
        manager_count = options["number_of_managers"]

        models = [PersonalAdvisor, YoungPerson, Manager, Goal, Action]
        for m in models:
            m.objects.all().delete()

        with factory.Faker.override_default_locale("en_GB"):
            ManagerFactory.create_batch(manager_count)
