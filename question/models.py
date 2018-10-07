from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from user.models import User


class Tag(models.Model):
    WEB = "WEB",
    PWN = "PWN",
    Reverse = "Reverse"
    Crypto = "Crypto"
    MISC = "MISC"

    tag_name = models.CharField(max_length=8, unique=True, primary_key=True)


# Create your models here.
class Question(models.Model):
    question_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    question_name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=256)
    link = models.CharField(max_length=256, null=True)

    score = models.IntegerField(default=200)
    solve_by = models.ManyToManyField(User, through="Solve")
    flag = models.CharField(max_length=32)

    def set_flag(self, plain_text_flag):
        self.flag = make_password(plain_text_flag)

    def check_flag(self, plain_text_flag):
        cipher_text_flag = self.flag
        return check_password(plain_text_flag, cipher_text_flag)


class Solve(models.Model):
    who_solve = models.ForeignKey(User, on_delete=models.CASCADE)
    which_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    time = models.TimeField(auto_now_add=True, blank=True)

    class Meta:
        unique_together = ["who_solve", "which_question"]
