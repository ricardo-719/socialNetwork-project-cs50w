from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chirp = models.CharField(max_length=280)
    likes = models.IntegerField()
    date = models.DateField()

class Profile(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    profilePic=models.CharField(max_length=250, null=True, blank=True)
    introduction=models.CharField(max_length=400)

class Follows(models.Model):
    follower=models.CharField(max_length=80)
    followed=models.CharField(max_length=80)