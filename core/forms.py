from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from core.models import (
    Action,
    ChangeEntry,
    CheckInQuestion,
    CheckinQuestionAnswer,
    Goal,
    ChecklistQuestionAnswer,
    Goal,
    Question,
    YoungPerson,
)


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

    def save(self, yp, user, commit=True):
        t = self.cleaned_data["title"]
        d = self.cleaned_data["description"]
        change_entry = ChangeEntry.objects.create(by=user)
        goal = Goal.objects.create(
            title=t,
            description=d,
            young_person=yp,
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
        goal = Goal.objects.get(pk=id)
        change_entry = ChangeEntry.objects.create(by=request.user)
        action = Action.objects.create(
            description=d, deadline=dead, goal=goal, created=change_entry
        )
        return action


class CheckinForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        questions = CheckInQuestion.objects.all()
        print(questions)
        for question in questions:
            self.fields[str(question.pk)] = forms.ChoiceField(
                label=question.text,
                widget=forms.RadioSelect,
                choices=CheckinQuestionAnswer.choices,
            )
            print(question.text)

           
class ChecklistForm(forms.Form):
    def __init__(self, *args, checklist, **kwargs):
        super().__init__(*args, **kwargs)
        questions = Question.objects.filter(checklist=checklist)
        for question in questions:
            self.fields[str(question.pk)] = forms.ChoiceField(
                label=question.text, choices=ChecklistQuestionAnswer.choices
            )
