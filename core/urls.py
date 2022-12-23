from django.urls import path

from core import views

urlpatterns = [
    path("", views.index, name="index"),
    path("yp", views.yp, name="yp"),
    path("invite", views.invite, name="invite"),
    path("goals", views.goals, name="goals"),
    path("create_goal", views.create_goal, name="create_goal"),
    path("goals/<int:goal_id>", views.edit_goal, name="edit_goal"),
    path("archive_goal/<int:goal_id>/", views.archive_goal, name="archive_goal"),
    path("complete_goal/<int:goal_id>/", views.complete_goal, name="complete_goal"),
    path("action/<int:action_id>", views.edit_action, name="edit_action"),
    path(
        "archive_action/<int:action_id>/", views.archive_action, name="archive_action"
    ),
    path(
        "complete_action/<int:action_id>/",
        views.complete_action,
        name="complete_action",
    ),
    path("checklist", views.checklist, name="checklist"),
    path(
        "checklist/<int:checklist_id>",
        views.checklist_questions,
        name="checklist_questions",
    ),
]
