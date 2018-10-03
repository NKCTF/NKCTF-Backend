from django.urls import path

from . import views


app_name = "user_search"
urlpatterns = [
    path("user/", views.SearchUser.as_view(), name="user"),
    path("team/", views.SearchTeam.as_view(), name="team"),
]
