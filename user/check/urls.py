from django.urls import path, include

from . import views


app_name = "check"
urlpatterns = [
    path("password/", views.Password.as_view(), name="password"),
]
