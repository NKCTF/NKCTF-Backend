from django.urls import path

from .import views


app_name = "scoreboard"
urlpatterns = [
    path("user/", views.user_score, name="user"),
    path("team/", views.team_score, name="team"),
]
