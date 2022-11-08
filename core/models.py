from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class MetadataMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    updated_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    completed_at = models.DateTimeField(null=True, editable=False)
    completed_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        abstract = True


class ChecklistQuestionAnswer(models.IntegerChoices):
    NO = 0, _("No")
    YES = 1, _("Yes")
    NOT_RELEVANT = 2, _("This isn't relevant to me")


class NoteType(models.IntegerChoices):
    PA = 0, _("Pathway Plan PA")
    MANAGER = 1, _("Pathway Plan Manager")


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="manager")


class PersonalAdvisor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="personal_advisor"
    )
    manager = models.ForeignKey(
        "PersonalAdvisor",
        related_name="personal_advisors",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )


class YoungPerson(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="young_person"
    )
    personal_advisors = models.ManyToManyField(
        PersonalAdvisor, related_name="young_persons"
    )


class Goal(MetadataMixin, models.Model):
    young_person = models.ForeignKey(
        YoungPerson, on_delete=models.CASCADE, related_name="goals"
    )
    archived = models.DateTimeField(null=True, blank=True)
    title = models.TextField(max_length=50)
    description = models.TextField(max_length=500, null=True, blank=True)


class Action(MetadataMixin, models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="actions")
    deadline = models.DateTimeField(null=True, blank=True)
    description = models.TextField(max_length=500)
    owner = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="owned_actions"
    )


class Checklist(models.Model):
    title = models.TextField(max_length=500)


class Question(models.Model):
    text = models.TextField(max_length=500)
    checklist = models.ForeignKey(
        Checklist, on_delete=models.CASCADE, related_name="checklist_questions"
    )


class ChecklistResponse(models.Model):
    checklist = models.ForeignKey(
        Checklist, on_delete=models.CASCADE, related_name="checklist_instances"
    )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="created_checklist_responses",
    )
    young_person = models.ForeignKey(
        YoungPerson, on_delete=models.CASCADE, related_name="checklist_responses"
    )
    note = models.TextField(max_length=500, null=True, blank=True)


class ChecklistQuestionResponse(models.Model):
    checklist_response = models.ForeignKey(
        ChecklistResponse,
        on_delete=models.CASCADE,
        related_name="checklist_question_response_instance",
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="question_responses"
    )
    answer = models.PositiveSmallIntegerField(choices=ChecklistQuestionAnswer.choices)
    note = models.TextField(max_length=500, null=True, blank=True)


class Note(models.Model):
    young_person = models.ForeignKey(
        YoungPerson, on_delete=models.CASCADE, related_name="notes"
    )
    submitted = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="submitted_notes"
    )
    note_type = models.PositiveSmallIntegerField(
        choices=NoteType.choices, null=True, blank=True
    )
