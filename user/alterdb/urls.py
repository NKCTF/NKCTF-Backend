from django.urls import path

from . import views


app_name = "user_alter"
urlpatterns = [
    path("alter_personal/", views.AlterPersonal.as_view(), name="alter_personal"),
    path("alter_team/", views.AlterTeam.as_view(), name="alter_team"),
    path("create_team/", views.CreateTeam.as_view(), name="create_team"),
    path("join_team/", views.JoinTeam.as_view(), name="join_team"),
    path("exe_application/", views.ExecuteApplication.as_view(), name="exe_appl")
]
