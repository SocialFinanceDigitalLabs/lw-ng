from django.urls import path

from . import views

urlpatterns = [
    path(f'{p["id"]}/', p["func"], name=p["id"]) for p in views.page.all.values()
]
