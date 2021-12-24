from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.datetime_safe import date

User = get_user_model()

def page_register():
    registry = {}

    def decorator(id, name):
        def caller(func):
            def callee(*args, **kwargs):
                nav = [dict(**n, current=n['id']==id) for n in registry.values()]
                return func(*args, **kwargs, nav=nav)

            registry[id] = dict(id=id, name=name, func=callee)
            return callee
        return caller

    decorator.all = registry
    return decorator


page = page_register()


@page(id='updates', name='Profile')
@login_required
def updates(request, nav):
    worker = User(username="peter.andre@la.gov.uk", first_name="Peter", last_name="Andre")
    worker.email = worker.username

    last_checkin = dict(id=1, date=date(2021, 12, 24))

    updates = [
        dict(date=date(2021, 10, 16), updates=[
            dict(user=worker, updates=[
                f"{worker.first_name} {worker.last_name} has completed some checklist questions about housing",
                f"{worker.first_name} {worker.last_name} has completed some checklist questions about health",
            ]),
        ]),
        dict(date=date(2021, 11, 2), updates=[
            dict(user=worker, updates=[
                f"{worker.first_name} {worker.last_name} has completed some checklist questions about housing",
            ]),
        ])
    ]

    context = dict(
        nav=nav,
        worker=worker,
        last_checkin=last_checkin,
        updates=updates,
    )

    return render(request, 'lw_yp/updates.html', context)


@page(id='goals', name='Goals')
@login_required
def goals(request, nav):
    return render(request, 'lw_yp/todo.html', dict(nav=nav))


@page(id='needs', name='Checklist')
@login_required
def needs(request, nav):
    return render(request, 'lw_yp/todo.html', dict(nav=nav))


@page(id='summary', name='Overview')
@login_required
def summary(request, nav):
    return render(request, 'lw_yp/todo.html', dict(nav=nav))


@page(id='archive', name='Archive')
@login_required
def archive(request, nav):
    return render(request, 'lw_yp/todo.html', dict(nav=nav))
