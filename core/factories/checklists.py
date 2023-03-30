import factory
from factory.django import DjangoModelFactory
from core.models import Goal, Action
from random import randint
from django.utils.timezone import get_current_timezone

class ChecklistResponseFactory(DjangoModelFactory):
    checklist =
    created =
    created_by =
    young_person =
    note = faker.Fake("Sentence")

    class Meta:
        model = ChecklistResponse

class ChecklistQuestionResponseFactory(DjangoModelFactory):
    checklist_response =
    question =
    answer =
    note = faker.Fake("Sentence")

    class Meta:
        model = ChecklistQuestionResponse