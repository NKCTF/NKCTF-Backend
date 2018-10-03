from django.urls import path

from . import views


app_name = "question"
urlpatterns = [
    path("lst", views.QuestionList.as_view()),
    path("msg", views.QuestionMessage.as_view()),
    path("flg", views.CheckFlag.as_view())
]
