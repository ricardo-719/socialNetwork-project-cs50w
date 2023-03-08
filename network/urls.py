
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("follow", views.handleFollow, name="follow"),
    path("following", views.following_view, name="following"),
    path("<str:name>", views.profile_view, name="profile")
]
