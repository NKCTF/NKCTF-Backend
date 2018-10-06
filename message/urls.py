from django.urls import path

from . import views


app_name = "massage"
urlpatterns = [
    path("mail_box/", views.MailBox.as_view(), name="mail_box"),
]
