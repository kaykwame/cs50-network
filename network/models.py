from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.fields import MoneyField
from django.conf import settings


class User(AbstractUser):
    Follow_status = models.BooleanField(default=False)

class Posts(models.Model):
    Poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    Poster_username = models.CharField(max_length=30)
    Post_content = models.TextField()
    Date_posted = models.DateTimeField(auto_now=False, auto_now_add=True)
    Likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')

    def serialize(self):
        return {
            "id": self.id,
            "Poster": self.Poster.posts,
            "Post_content": self.Post_content,
            "Date_posted": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "Liked": self.Liked
        }

class Likes(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, related_name='likes', on_delete=models.CASCADE)

class Followers(models.Model):
    class Meta:
        unique_together = ["followee", "follower"]
    followee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followerr")
