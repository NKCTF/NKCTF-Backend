from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from user.models import User


# Create your models here.
class Question(models.Model):
    possible_tag = (
        (0, "WEB"),
        (1, "PWN"),
        (2, "Reverse"),
        (3, "Crypto"),
        (4, "MISC"),
    )
    tag = models.CharField(max_length=32, choices=possible_tag)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    link = models.CharField(max_length=256)

    score = models.IntegerField(default=200)
    flag = models.CharField(max_length=32)

    def set_flag(self, plain_text_flag):
        self.flag = make_password(plain_text_flag)

    def check_flag(self, plain_text_flag):
        cipher_text_flag = self.flag
        return check_password(plain_text_flag, cipher_text_flag)


class Solve(models.Model):
    who_solve = models.ForeignKey(User, on_delete=models.CASCADE)
    which_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    time = models.TimeField()
