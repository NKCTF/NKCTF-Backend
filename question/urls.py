from django.urls import path

from . import views


app_name = "question"
urlpatterns = [
    path("lst", views.question_lst),
    path("msg", views.question_msg),
    path("flag", views.question_flag)
]
