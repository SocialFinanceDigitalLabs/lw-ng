from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from core import permissions
from core.models import Action, ChangeEntry, Goal, YoungPerson


class NewYoungPersonForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=False)

    def save(self, commit=True):
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        user = User.objects.create(
            username=f"{first_name}.{last_name}",
            first_name=first_name,
            last_name=last_name,
        )
        yp = YoungPerson.objects.create(user=user)
        return yp


class NewGoalForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50, required=True)
    description = forms.CharField(label="Description", max_length=500, required=True)

    def __init__(self, young_person_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.young_person_id = young_person_id

    def save(self, request, commit=True):
        if permissions.is_young_person(request.user):
            young_person = request.user.young_person
        else:
            young_person = YoungPerson.objects.get(id=self.young_person_id)
        t = self.cleaned_data["title"]
        d = self.cleaned_data["description"]
        change_entry = ChangeEntry.objects.create(by=request.user)
        goal = Goal.objects.create(
            title=t,
            description=d,
            young_person=young_person,
            created=change_entry,
        )
        return goal


class GoalEditForm(ModelForm):
    class Meta:
        model = Goal
        fields = ["title", "description"]


class ActionEditForm(ModelForm):
    class Meta:
        model = Action
        fields = ["description", "deadline"]


class NewActionForm(forms.Form):
    description = forms.CharField(label="Description", max_length=500, required=True)
    deadline = forms.DateTimeField(
        widget=forms.DateInput(
            attrs={"class": "datepicker"},
        ),
        label="Deadline",
        required=True,
    )
    iden = forms.IntegerField(widget=forms.HiddenInput, initial=True)

    def save(self, request, commit=True):
        d = self.cleaned_data["description"]
        id = self.cleaned_data["iden"]
        dead = self.cleaned_data["deadline"]
        for goal in request.user.young_person.goals.all():
            if goal.id == id:
                change_entry = ChangeEntry.objects.create(by=request.user)
                action = Action.objects.create(
                    description=d, deadline=dead, goal=goal, created=change_entry
                )
                return action
