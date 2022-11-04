from django.shortcuts import render, redirect
from .forms import NewYoungPersonForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "core/index.html")

@login_required
def yp(request):
    pa = request.user.personal_advisor
    return render(request, "core/yp.html", context = dict(pa = pa))

@login_required
def invite(request):
    pa = request.user.personal_advisor
    if request.method == "POST":
        form = NewYoungPersonForm(request.POST)
        if form.is_valid():
            yp = form.save()
            pa.young_persons.add(yp)
            messages.success(request, "Registration successful." )
            return redirect("yp")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewYoungPersonForm()
    return render (request=request, template_name="core/invite.html", context={"register_form":form, "pa":pa})