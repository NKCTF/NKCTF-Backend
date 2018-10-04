from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=128, default='Join our team!!')

    def agree_apply(self, user):
        if list(user.filter(apply_for=self)) is []:
            raise Exception("Current user doesn't apply for this team")
        user.apply_for.clear()
        user.belong = self
        user.save()

    def reject_apply(self, user):
        if list(user.filter(apply_for=self)) is []:
            raise Exception("Current user doesn't apply for this team")
        user.apply_for.remove(self)


class Career(models.Model):
    WEB = "WEB, 网络"
    PWN = "PWN, 二进制"
    Reverse = "Reverse, 逆向"
    Crypto = "Crypto, 密码学"
    MISC = "MISC, 杂项"
    Almighty = "Almighty, 万精油"

    career_name = models.CharField(max_length=16, unique=True, primary_key=True)


class User(AbstractUser):
    """从 Django 系统定义的抽象基类 AbstractUser 派生出我们自己的类"""
    auth_id = models.IntegerField(unique=True, null=True)
    auth_type = models.CharField(max_length=16, null=True)

    score = models.IntegerField(default=0)
    qq = models.CharField(max_length=16, null=True)
    github = models.CharField(max_length=32, null=True)
    description = models.CharField(max_length=128, default='Welcome to NanKai CTF')

    belong = models.ForeignKey(Team, on_delete=models.SET_NULL,
                               related_name="work_for", null=True)
    user_career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True)
    join_date = models.DateField(null=True)
    is_leader = models.BooleanField(default=False, null=True)

    apply_for = models.ManyToManyField(Team, related_name="apply_for")

    def send_application(self, team):
        if self.belong is not None:
            raise Exception("User have joined a team!")
        self.apply_for.add(team)
