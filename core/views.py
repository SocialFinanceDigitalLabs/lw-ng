from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render

from core.builder import create_random_users
from core.forms import FactoryForm, NewYoungPersonForm


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


def factory(request):
    if request.POST:
        form = FactoryForm(request.POST)
        if form.is_valid():
            try:
                data = create_random_users(
                    form.cleaned_data["manager_count"],
                    form.cleaned_data["pa_count"],
                    form.cleaned_data["yp_count"],
                )
                messages.success(request, "users successfully created!")
                return render(request, "core/factory/list.html", {"data": data})
            except IntegrityError:
                # if the usernames are not unique, try again
                messages.error(request, "something went wrong - please try again")

    form = FactoryForm()
    return render(request, "core/factory/create.html", {"form": form})
