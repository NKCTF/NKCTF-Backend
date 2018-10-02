from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """从 Django 系统定义的抽象基类 AbstractUser 派生出我们自己的类"""
    Auth_ID = models.IntegerField(unique=True)
    Auth_Type = models.CharField(max_length=16, null=True)

    Score = models.IntegerField(default=0)
    QQ = models.CharField(max_length=16, null=True)
    Github = models.CharField(max_length=32, null=True)
    Description = models.CharField(max_length=128, default='Welcome to NanKai CTF')


class Team(models.Model):
    Name = models.CharField(max_length=32, unique=True)
    Description = models.CharField(max_length=128, default='Join our team!!')
    Leader = models.ForeignKey(User, on_delete=models.CASCADE)


class Join(models.Model):
    WhoJoin = models.ForeignKey(User, on_delete=models.CASCADE)
    WhichTeam = models.ForeignKey(Team, on_delete=models.CASCADE)
    Time = models.TimeField()
