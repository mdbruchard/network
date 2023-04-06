from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", blank=True, null=True, symmetrical=False, related_name="follow")
    followers = models.ManyToManyField("self", blank=True, null=True, symmetrical=False, related_name="follower")




class Post(models.Model):
    post = models.CharField(max_length=256, default="New Post")
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_name")
    like = models.ManyToManyField(User, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "post": self.post,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "like": [User.username for User in self.like.all()]
        }
