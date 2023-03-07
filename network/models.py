from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chirp = models.CharField(max_length=280)
    likes = models.IntegerField(default=0)
    date = models.DateField()
    time = models.TimeField()

class Profile(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    username=models.CharField(max_length=80)
    profilePic=models.CharField(max_length=250, null=True, blank=True, default="https://th.bing.com/th/id/OIP.ybB2a0HimX1I-ybBY4pOPwHaHa?pid=ImgDet&rs=1")
    introduction=models.CharField(max_length=400, default="")
    numFollower=models.IntegerField(default=0)
    numFollowing=models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Follows(models.Model):
    follower=models.CharField(max_length=80)
    followed=models.CharField(max_length=80)