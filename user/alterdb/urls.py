from django.urls import path

from . import views


app_name = "user_alter"
urlpatterns = [
    path("personal/", views.AlterPersonal.as_view(), name="personal"),
]
