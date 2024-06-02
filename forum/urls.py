from django.urls import path
from . import views


app_name = "forum"

urlpatterns = [
    path("", views.discussions_list, name="discussions_list"),
    path("discussion/<int:pk>/", views.discussion_detail, name="discussion_detail"),
    path("create_discussion/", views.create_discussion, name="create_discussion"),
    path("discussion/<int:pk>/create_post/", views.create_post, name="create_post"),
    path("post/<int:pk>/edit/", views.edit_post, name="edit_post"),
    path("post/<int:pk>/delete/", views.delete_post, name="delete_post"),
    path(
        "notification/read/<int:notification_id>/",
        views.read_notification,
        name="read_notification",
    ),
]
