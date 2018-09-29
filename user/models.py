from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
class Team(models.Model):
    Name = models.CharField(max_length=32, unique=True)
    Description = models.CharField(max_length=128, default='Join our team!!')


class User(models.Model):
    Auth_Offer = (
        (1, "GitHub"),
        (2, "QQ"),
        (3, "Google"),
        (4, "NK-Count"),
    )
    Auth_Token = models.CharField(max_length=32, null=True)
    Auth_Type = models.CharField(max_length=16, choices=Auth_Offer, null=True)

    Name = models.CharField(max_length=32, unique=True)
    Password = models.CharField(max_length=64)
    Score = models.IntegerField(default=0)
    QQ = models.CharField(max_length=16, null=True)
    Description = models.CharField(max_length=128, default='Welcome to NanKai CTF')
    Email = models.CharField(max_length=32, null=True)
    BelongTo = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
