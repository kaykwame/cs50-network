from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("allposts", views.allposts, name="allposts"),
    path("follow/<int:userid>", views.follow, name="follow"),
    path("unfollow/<int:userid>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("profilepage/<str:poster>", views.profilepage, name="profilepage"),

    #API Routes
    path("post/<int:post_id>", views.post, name="post"),
    path('like/', views.like, name='post-like'),
]
