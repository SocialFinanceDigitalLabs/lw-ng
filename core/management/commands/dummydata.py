from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import factory
from core.factories.people import ManagerFactory
from django.core.management import call_command

from core.models import PersonalAdvisor, YoungPerson, Manager, Goal, Action, Checklist, Question

User = get_user_model()


class Command(BaseCommand):
    help = "Deletes all data in user defined models"

    def add_arguments(self, parser):
        parser.add_argument("number_of_managers", type=int, default=100)

    def handle(self, *args, **options):
        manager_count = options["number_of_managers"]

        models = [PersonalAdvisor, YoungPerson, Manager, Goal, Action, Question, Checklist]
        for m in models:
            m.objects.all().delete()

        call_command("loaddata", "checklists")

        with factory.Faker.override_default_locale("en_GB"):
            ManagerFactory.create_batch(manager_count)

        print("\33[41m Created the following Managers: \33[0m")
        managers = Manager.objects.all()
        for manager in managers:
            print("{}".format(manager.user.username))

        print("\33[42m Created the following PAs: \33[0m")
        pas = PersonalAdvisor.objects.all()
        for pa in pas:
            print("{}".format(pa.user.username))

        print("\33[44m Created the following YPs: \33[0m")
        yps = YoungPerson.objects.all()
        for yp in yps:
            print("{}".format(yp.user.username))
