from django.db import models
from user.models import User, Team
from datetime import datetime  # 用于设置加入队伍的时间

class AbstractMail(models.Model):
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=256)
    is_read = models.BooleanField(default=False)
    send_time = models.TimeField(auto_now_add=True, blank=True)
    send_to = models.ForeignKey(User, related_name="mail_send_to", on_delete=models.CASCADE)
    send_by = models.ForeignKey(User, related_name="mail_send_by", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Mail(AbstractMail):
    pass


class JoinRequest(AbstractMail):
    send_to = models.ForeignKey(Team, related_name="join_to_team", on_delete=models.CASCADE)
    send_by = models.ForeignKey(User, related_name="join_by_user", on_delete=models.CASCADE)
    agree = models.BooleanField(null=True)

    def save(self, *args, **kwargs):
        """
        在 JoinRequest 对象存入数据库前检测，send_by 一个这个用户是否已经加入一个战队
        """
        if self.send_by.belong is not None:
            raise ValueError("The send_by field User have joined a team yet!")
        else:
            super(JoinRequest, self).save(*args, **kwargs)

    class Meta:
        unique_together = ["send_by", "send_to"]

    def execute_apply(self, is_agree):
        """
        处理一个加入战队的申请
        :param is_agree: 是否同意加入战队，同意为 True，拒绝为 False
        """
        sender = self.send_by
        # TODO: 如果发送邮件的人已经加入一个战队了，引发一个错误
        if sender.belong is not None:
            # TODO: 如果同意了，则将发送请求的人设置为已经加入了战队
            if is_agree:
                sender.belong = self
                sender.join_date = datetime.now()
                sender.save()
        else:
            raise Exception("This user has been belonged to a team.")
        # TODO: request_mail 已经读取并设置是否同意
        self.agree = is_agree
        self.is_read = True
        self.save()
        # TODO: 返回发送一个告知是否同意的邮件
        response_mail = Mail.objects.create(
            send_by=User.objects.get(is_leader=True, belong=self.send_to),  # send_by 本战队的队长
            send_to=sender,  # send_to request_mail 的发送人
        )
        response_mail.title = f"{self.send_to.team_name} have " \
                              f"{'agreed' if is_agree else 'refused'}" \
                              f" your join request."
        response_mail.content = f"Welcome to {self.send_to.team_name}" if is_agree else \
                                f"Sorry to refuse you to join {self.send_to.team_name}."
        response_mail.save()
