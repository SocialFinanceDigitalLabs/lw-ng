from django import forms
from django.contrib.auth.models import User

from core.models import Action, Goal, YoungPerson


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
    goal_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def save(self, request, commit=True):
        t = self.cleaned_data["title"]
        d = self.cleaned_data["description"]
        goal = Goal.objects.create(
            title=t,
            description=d,
            young_person=request.user.young_person,
        )
        return goal


class NewActionForm(forms.Form):
    description = forms.CharField(label="Description", max_length=500, required=True)
    deadline = forms.DateTimeField(
        widget=forms.DateInput(
            attrs={"class": "datepicker"},
        ),
        label="Deadline",
        required=True,
    )
    iden = forms.IntegerField(widget=forms.HiddenInput)
    action_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def save(self, request, commit=True):
        d = self.cleaned_data["description"]
        id = self.cleaned_data["iden"]
        dead = self.cleaned_data["deadline"]
        for goal in request.user.young_person.goals.all():
            if goal.id == id:
                action = Action.objects.create(description=d, deadline=dead, goal=goal)
                return action


class CompleteGoalForm(forms.Form):
    goal_i = forms.IntegerField(widget=forms.HiddenInput)
    g_complete = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def save(self, commit=True):
        id = self.cleaned_data["goal_i"]
        g = Goal.objects.filter(id=id).update(complete=True)
        return g


class ArchiveGoalForm(forms.Form):
    goal_i = forms.IntegerField(widget=forms.HiddenInput)
    g_archive = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def save(self, commit=True):
        id = self.cleaned_data["goal_i"]
        g = Goal.objects.filter(id=id).update(archived=True)
        return g
