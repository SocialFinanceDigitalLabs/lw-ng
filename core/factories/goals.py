import factory
from factory.django import DjangoModelFactory
from core.models import Goal, Action
from random import randint
from django.utils.timezone import get_current_timezone


class ActionFactory(DjangoModelFactory):
    deadline = factory.Faker(
        "date_time_this_month",
        before_now=False,
        after_now=True,
        tzinfo=get_current_timezone(),
    )
    description = factory.Faker(
        "paragraph", nb_sentences=3, variable_nb_sentences=False
    )
    owner = None  # Can be tricky to randomly pick PA or YA for creation
    completed = None
    archived = None

    class Meta:
        model = Action


class GoalFactory(DjangoModelFactory):
    completed = None
    archived = None
    title = factory.Faker("paragraph", nb_sentences=1, variable_nb_sentences=False)
    description = factory.Faker(
        "paragraph", nb_sentences=3, variable_nb_sentences=False
    )

    goals = factory.RelatedFactoryList(
        ActionFactory, factory_related_name="goal", size=lambda: randint(2, 5)
    )

    class Meta:
        model = Goal
