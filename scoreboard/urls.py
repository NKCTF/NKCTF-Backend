from django.urls import path

from .import views


app_name = "scoreboard"
urlpatterns = [
    path("user/", views.UserScore.as_view(), name="user"),
    path("team/", views.TeamScore.as_view(), name="team"),
]
