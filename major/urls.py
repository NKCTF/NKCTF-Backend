from django.urls import path

from . import views


app_name = "major"
urlpatterns = [
    path("", views.major_page, name="index"),
]
