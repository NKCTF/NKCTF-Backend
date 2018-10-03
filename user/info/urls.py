from django.urls import path

from . import views


app_name = "user_info"
urlpatterns = [
    path("user/", views.UserInformation.as_view(), name="user"),
    path("team/", views.TeamInformation.as_view(), name="team"),
]
