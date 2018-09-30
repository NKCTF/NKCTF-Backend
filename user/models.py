# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    Auth_Offer = (
        (1, "GitHub"),
        (2, "QQ"),
    )
    Auth_Token = models.CharField(max_length=32, null=True)
    Auth_Type = models.CharField(max_length=16, choices=Auth_Offer, null=True)

    Score = models.IntegerField(default=0)
    QQ = models.CharField(max_length=16, null=True)
    Github = models.CharField(max_length=32, null=True)
    Description = models.CharField(max_length=128, default='Welcome to NanKai CTF')
    Email = models.CharField(max_length=32, null=True)


class Team(models.Model):
    Name = models.CharField(max_length=32, unique=True)
    Description = models.CharField(max_length=128, default='Join our team!!')
    Leader = models.ForeignKey(Member, on_delete=models.CASCADE)
    #Join_Team = models.ManyToManyField(Member)

