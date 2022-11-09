from django.urls import path

from core import views

urlpatterns = [
    path("", views.index, name="index"),
    path("yp", views.yp, name="yp"),
    path("invite", views.invite, name="invite"),
    path("factory", views.factory, name="factory"),
]
