from django.urls import path

from . import views


app_name = "user"
urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("signup/", views.Signup.as_view(), name="signup"),
    path("auth_in/", views.user_auth_in, name="auth_in"),
    path("auth_back/", views.AuthLogin.as_view(), name="auth_back"),
]
