from core.factories.goals import GoalFactory
from core.factories.checklists import ChecklistFactory
from random import randint
from django.db.models.signals import post_save
from factory.django import DjangoModelFactory
import factory
from core.models import PersonalAdvisor, YoungPerson, Manager

from django.contrib.auth import get_user_model

User = get_user_model()
DEFAULT_PASSWORD = "somePassword!"


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("email")
    email = username
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    plaintext_password = factory.PostGenerationMethodCall(
        "set_password", DEFAULT_PASSWORD
    )

    class Meta:
        model = User
        exclude = ("plaintext_password",)


class YoungPersonFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    # Goal Generation
    goals = factory.RelatedFactoryList(
        GoalFactory, factory_related_name="young_person", size=lambda: randint(2, 5)
    )

    # Checklist Generation: Add individual checklist data here

    @factory.post_generation
    def personal_advisors(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, do nothing.
            return

        self.personal_advisors.add(extracted)

    class Meta:
        model = YoungPerson


class PersonalAdvisorFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    yps = factory.RelatedFactoryList(
        YoungPersonFactory,
        factory_related_name="personal_advisors",
        size=lambda: randint(2, 5),
    )

    class Meta:
        model = PersonalAdvisor


class ManagerFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    pas = factory.RelatedFactoryList(
        PersonalAdvisorFactory,
        factory_related_name="manager",
        size=lambda: randint(2, 5),
    )

    class Meta:
        model = Manager
