from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from core import permissions

from .forms import (
    ActionEditForm,
    ChangeEntry,
    GoalEditForm,
    NewActionForm,
    NewGoalForm,
    NewYoungPersonForm,
)
from .models import Action, Checklist, Goal, YoungPerson


@login_required
def index(request):
    if permissions.is_manager(request.user):
        return render(request, "core/manager/index.html")
    elif permissions.is_personal_advisor(request.user):
        return render(request, "core/pa/index.html")
    elif permissions.is_young_person(request.user):
        return render(request, "core/yp/index.html")


@login_required
def index_yp(request, young_person_id):
    if permissions.is_manager(request.user) or permissions.is_personal_advisor(
        request.user
    ):
        yp = YoungPerson.objects.get(pk=young_person_id)
        user = request.user
        return render(
            request,
            "core/yp/index.html",
            context={
                "yp": yp,
                "user": user,
            },
        )
    else:
        return redirect("index")


@login_required
def yp(request):
    pa = request.user.personal_advisor
    return render(request, "core/yp.html", context=dict(pa=pa))


@login_required
def invite(request):
    pa = request.user.personal_advisor
    if request.method == "POST":
        form = NewYoungPersonForm(request.POST)
        if form.is_valid():
            yp = form.save()
            pa.young_persons.add(yp)
            messages.success(request, "Registration successful.")
            return redirect("yp")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewYoungPersonForm()
    return render(
        request=request,
        template_name="core/invite.html",
        context={"register_form": form, "pa": pa},
    )


@login_required
def create_goal(request):
    yp = request.user.young_person
    goal_form = NewGoalForm()
    if request.method == "POST":
        goal_form = NewGoalForm(request.POST)
        if goal_form.is_valid():
            goal_form.save(request)
            messages.success(request, "Goal saved.")
            return redirect("goals")
        else:
            messages.error(request, "Goal not saved. Invalid information.")
            return redirect("goals")

    context = {
        "goal_form": goal_form,
        "yp": yp,
    }
    return render(request, template_name="core/yp/create_goal.html", context=context)


@login_required
def goals(request):
    user = request.user
    yp = request.user.young_person
    current_goals = request.user.young_person.goals.filter(
        completed__isnull=True, archived__isnull=True
    )
    complete_goals = request.user.young_person.goals.filter(
        completed__isnull=False, archived__isnull=True
    )
    action_form = NewActionForm()
    if request.method == "POST":
        action_form = NewActionForm(request.POST)
        if action_form.is_valid():
            action_form.save(request)
            messages.success(request, "Action saved.")
            return redirect("goals")
        else:
            messages.error(request, "Action not saved. Invalid information.")
            return redirect("goals")
    else:
        pass
    context = {
        "action_form": action_form,
        "yp": yp,
        "current_goals": current_goals,
        "complete_goals": complete_goals,
        "user": user,
    }
    return render(request, template_name="core/yp/goals.html", context=context)


@login_required
def yp_goals(request, young_person_id):
    user = request.user
    yp = YoungPerson.objects.get(pk=young_person_id)
    current_goals = yp.goals.filter(completed__isnull=True, archived__isnull=True)
    complete_goals = yp.goals.filter(completed__isnull=False, archived__isnull=True)
    action_form = NewActionForm()
    if request.method == "POST":
        action_form = NewActionForm(request.POST)
        if action_form.is_valid():
            action_form.save(request)
            messages.success(request, "Action saved.")
            return redirect("goals")
        else:
            messages.error(request, "Action not saved. Invalid information.")
            return redirect("goals")
    else:
        pass
    context = {
        "action_form": action_form,
        "yp": yp,
        "current_goals": current_goals,
        "complete_goals": complete_goals,
        "user": user,
    }
    return render(request, template_name="core/yp/goals.html", context=context)


@login_required
def edit_goal(request, goal_id):
    yp = request.user.young_person
    try:
        goal = Goal.objects.get(pk=goal_id)
    except Goal.DoesNotExist:
        raise Http404("Goal does not exist")
    form = GoalEditForm(instance=goal)
    if request.method == "POST":
        form = GoalEditForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, "Goal updated.")
            return redirect("goals")
        else:
            messages.error(request, "Goal not saved. Invalid information.")
    else:
        pass
    context = {
        "goal": goal,
        "yp": yp,
        "goal_edit_form": form,
    }
    return render(request, template_name="core/yp/edit_goal.html", context=context)


@login_required
def archive_goal(request, goal_id):
    try:
        change_entry = ChangeEntry.objects.create(by=request.user)
        Goal.objects.filter(id=goal_id).update(archived=change_entry)
        messages.success(request, "Goal archived.")
    except Goal.DoesNotExist:
        messages.error(request, "Goal not archived.")
    return redirect("goals")


@login_required
def complete_goal(request, goal_id):
    try:
        change_entry = ChangeEntry.objects.create(by=request.user)
        Goal.objects.filter(id=goal_id).update(completed=change_entry)
        messages.success(request, "Goal completed.")
    except Goal.DoesNotExist:
        messages.error(request, "Goal not completed.")
    return redirect("goals")


@login_required
def edit_action(request, action_id):
    yp = request.user.young_person
    try:
        action = Action.objects.get(pk=action_id)
    except action.DoesNotExist:
        raise Http404("Action does not exist")
    form = ActionEditForm(instance=action)
    if request.method == "POST":
        form = ActionEditForm(request.POST, instance=action)
        if form.is_valid():
            form.save()
            messages.success(request, "Action updated.")
            return redirect("goals")
        else:
            messages.error(request, "Action not saved. Invalid information.")
    else:
        pass
    context = {
        "action": action,
        "yp": yp,
        "action_edit_form": form,
    }
    return render(request, template_name="core/yp/edit_action.html", context=context)


@login_required
def archive_action(request, action_id):
    try:
        change_entry = ChangeEntry.objects.create(by=request.user)
        Action.objects.filter(id=action_id).update(archived=change_entry)
        messages.success(request, "Action archived.")
    except Action.DoesNotExist:
        messages.error(request, "Action not archived.")
    return redirect("goals")


@login_required
def complete_action(request, action_id):
    try:
        change_entry = ChangeEntry.objects.create(by=request.user)
        Action.objects.filter(id=action_id).update(completed=change_entry)
        messages.success(request, "Action completed.")
    except Action.DoesNotExist:
        messages.error(request, "Action not completed.")
    return redirect("goals")


@login_required
def checklist(request):
    yp = request.user.young_person
    checklist = Checklist.objects.all()
    context = {
        "yp": yp,
        "checklist": checklist,
    }
    return render(request, template_name="core/yp/checklist.html", context=context)


@login_required
def checklist_questions(request, checklist_id):
    yp = request.user.young_person
    try:
        checklist = Checklist.objects.get(pk=checklist_id)
        questions = checklist.checklist_questions.all()
    except checklist.DoesNotExist:
        raise Http404("Checklist does not exist")
    context = {
        "yp": yp,
        "questions": questions,
    }
    return render(
        request, template_name="core/yp/checklist_questions.html", context=context
    )
