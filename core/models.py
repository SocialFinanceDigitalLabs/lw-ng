from auditlog.registry import auditlog
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class AuditEntry(models.Model):
    at = models.DateTimeField(auto_now_add=True, editable=False)
    by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        abstract = True


class ChecklistQuestionAnswer(models.TextChoices):
    NO = "NO", _("No")
    YES = "YES", _("Yes")
    NOT_RELEVANT = "NOT", _("This isn't relevant to me")


class NoteType(models.TextChoices):
    PA = "PA", _("Pathway Plan PA")
    MANAGER = "MANAGER", _("Pathway Plan Manager")


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


class Goal(models.Model):
    young_person = models.ForeignKey(
        YoungPerson, on_delete=models.CASCADE, related_name="goals"
    )
    archived = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    title = models.TextField(max_length=50)
    description = models.TextField(max_length=500, null=True, blank=True)


auditlog.register(Goal)


class Action(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="actions")
    deadline = models.DateTimeField(null=True, blank=True)
    description = models.TextField(max_length=500)
    owner = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="owned_actions"
    )
    archived = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)


auditlog.register(Action)


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
    answer = models.CharField(
        choices=ChecklistQuestionAnswer.choices,
        max_length=3,
        default=ChecklistQuestionAnswer.NOT_RELEVANT,
    )
    note = models.TextField(max_length=500, null=True, blank=True)


class Note(models.Model):
    young_person = models.ForeignKey(
        YoungPerson, on_delete=models.CASCADE, related_name="notes"
    )
    submitted = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="submitted_notes"
    )
    note_type = models.CharField(
        choices=NoteType.choices, max_length=8, default=NoteType.PA
    )
