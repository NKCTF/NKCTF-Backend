from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Team(models.Model):
    Name = models.CharField(max_length=32, unique=True)
    Description = models.CharField(max_length=128, default='Join our team!!')


class User(AbstractUser):
    """从 Django 系统定义的抽象基类 AbstractUser 派生出我们自己的类"""
    Auth_ID = models.IntegerField(unique=True, null=True)
    Auth_Type = models.CharField(max_length=16, null=True)

    Score = models.IntegerField(default=0)
    QQ = models.CharField(max_length=16, null=True)
    Github = models.CharField(max_length=32, null=True)
    Description = models.CharField(max_length=128, default='Welcome to NanKai CTF')
    belong = models.ForeignKey(Team, on_delete=models.CASCADE)

    Join_Team = models.ManyToManyField(Team, through="Join")


class Join(models.Model):
    PossibleDirection = (
        (0, "WEB, 网络"),
        (1, "PWN, 二进制"),
        (2, "Reverse, 逆向"),
        (3, "Crypto, 密码学"),
        (4, "MISC, 杂项"),
        (5, "Almighty, 万精油")
    )
    Career = models.CharField(max_length=32, choices=PossibleDirection)
    WhoJoin = models.ForeignKey(User, on_delete=models.CASCADE)
    WhichTeam = models.ForeignKey(Team, on_delete=models.CASCADE)
    WhenJoin = models.DateField()
    IsLeader = models.BooleanField(default=False)
