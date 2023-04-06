
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("all-posts", views.allposts, name="allposts"),
    path("likes/<int:post_id>", views.likes, name="likes"),
    path("<int:profile>", views.profile, name="profile"),
    path("following/<int:profile>", views.follow, name="follow"),

    path("edit/<int:post_id>", views.edit, name="edit"),
]
