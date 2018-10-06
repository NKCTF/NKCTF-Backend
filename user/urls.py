from django.urls import path, include

from . import views


app_name = "user"
urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("signup/", views.Signup.as_view(), name="signup"),
    path("logout/", views.logout, name="logout"),
    path("auth_in/", views.user_auth_in, name="auth_in"),
    path("auth_back/", views.AuthLogin.as_view(), name="auth_back"),
    path("check/", include("user.check.urls")),
    path("info/", include("user.info.urls")),
    path("search/", include("user.search.urls")),
    path("alter/", include("user.alterdb.urls")),
]
