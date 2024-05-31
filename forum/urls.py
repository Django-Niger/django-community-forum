from django.urls import path
from .views import discussions_list, discussion_detail


app_name = "forum"

urlpatterns = [
    path("", discussions_list, name="discussions_list"),
    path("discussion/<int:pk>/", discussion_detail, name="discussion_detail"),
]
