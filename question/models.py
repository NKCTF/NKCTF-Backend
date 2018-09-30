from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from user.models import Member


# Create your models here.
class Question(models.Model):
    PossibleTag = (
        (0, "WEB"),
        (1, "PWN"),
        (2, "Reverse"),
        (3, "Crypto"),
        (4, "MISC"),
    )
    Tag = models.CharField(choices=PossibleTag)
    Name = models.CharField(max_length=32)
    Description = models.CharField(max_length=256)
    Link = models.CharField(max_length=256)

    Score = models.IntegerField(default=200)
    Flag = models.CharField(max_length=32)

    def set_flag(self, plain_text_flag):
        self.Flag = make_password(plain_text_flag)

    def check_flag(self, plain_text_flag):
        cipher_text_flag = self.Flag
        return check_password(plain_text_flag, cipher_text_flag)


class Solve(models.Model):
    WhoSolve = models.ForeignKey(Member, on_delete=models.CASCADE)
    WhichQuestion = models.ForeignKey(Question, on_delete=models.CASCADE)
    Time = models.TimeField()
