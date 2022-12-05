from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import (
    ArchiveGoalForm,
    CompleteGoalForm,
    NewActionForm,
    NewGoalForm,
    NewYoungPersonForm,
)


def index(request):
    return render(request, "core/index.html")


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
def goals(request):
    yp = request.user.young_person
    current_goals = request.user.young_person.goals.filter(completed_by__isnull=True)
    complete_goals = request.user.young_person.goals.filter(completed_by__isnull=False)
    goal_form = NewGoalForm()
    action_form = NewActionForm()
    g_complete = CompleteGoalForm()
    g_archive = ArchiveGoalForm()
    if request.method == "POST":
        if "goal_form" in request.POST:
            goal_form = NewGoalForm(request.POST)
            if goal_form.is_valid():
                goal_form.save(request)
                messages.success(request, "Goal saved.")
                return redirect("goals")
            else:
                messages.error(request, "Goal not saved. Invalid information.")
                return redirect("goals")
        if "g_complete" in request.POST:
            g_complete = CompleteGoalForm(request.POST)
            if g_complete.is_valid():
                g_complete.save(request)
                messages.success(request, "Achievement reached.")
                return redirect("goals")
            else:
                messages.error(request, "Goal not marked as complete.")
                return redirect("goals")
        if "g_archive" in request.POST:
            g_archive = ArchiveGoalForm(request.POST)
            if g_archive.is_valid():
                g_archive.save(request)
                messages.success(request, "Goal archived.")
                return redirect("goals")
            else:
                messages.error(request, "Goal not archived.")
                return redirect("goals")
        if "action_form" in request.POST:
            action_form = NewActionForm(request.POST)
            if action_form.is_valid():
                action_form.save(request)
                messages.success(request, "Action saved.")
                return redirect("goals")
            else:
                messages.error(request, "Action not saved. Invalid information.")
                return redirect("goals")
        else:
            messages.error(request, "form not found")
    else:
        pass
    context = {
        "goal_form": goal_form,
        "action_form": action_form,
        "g_complete": g_complete,
        "g_archive": g_archive,
        "yp": yp,
        "current_goals": current_goals,
        "complete_goals": complete_goals,
    }
    return render(request, template_name="core/goals.html", context=context)


@login_required
def action(request):
    yp = request.user.young_person
    if request.method == "POST":
        form = NewActionForm(request.POST)
        if form.is_valid():
            form.save(request)
            messages.success(request, "Action saved.")
            return redirect("goals")
        messages.error(request, "Action not saved. Invalid information.")
    else:
        form = NewActionForm()
    return render(
        request, template_name="action", context={"action_form": form, "yp": yp}
    )
