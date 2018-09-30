from django.urls import path

from . import views


app_name = "user"
urlpatterns = [
    path("login", views.user_login),
    path("signup", views.user_signup),
]
