from django.urls import path

from . import views


app_name = "check"
urlpatterns = [
    path("password/", views.Password.as_view(), name="password"),
    path("username/", views.Username.as_view(), name="username"),
]
