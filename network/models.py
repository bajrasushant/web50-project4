from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="userFollowing"
    )
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="userFollows"
    )


class Post(models.Model):
    description = models.TextField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poster} posted on {self.posted}"
