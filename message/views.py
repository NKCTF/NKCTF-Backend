from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import JoinRequest, Mail
from user.models import User


def JsonResponseZh(json_data):
    """
    因为返回含中文的 Json 数据总是需要设置 {'ensure_ascii': False}，所以直接在此集成
    :param json_data: 需要返回的数据
    """
    return JsonResponse(json_data, json_dumps_params={'ensure_ascii': False})


class MailBox(View):
    error = data = code = crt_team = crt_user = None
    normal_mail = join_request = []

    def get_ret_code(self):
        return {
            0: {"code": 0, "msg": "邮箱",
                "data": self.data},
            1: {"code": 1, "msg": "数据库查询错误",
                "error": self.error},
            2: {"code": 2, "msg": "只有队长拥有查询权限"},
            10: {"code": 10, "msg": "检测到攻击"},
            401: {"code": 401, "msg": "未授权用户"},
        }[self.code]

    def get_mail(self):
        try:
            # TODO: 读取普通邮件邮箱
            self.normal_mail = Mail.objects.filter(send_to=self.crt_user). \
                values("title", "content", "send_by", "send_time", "is_read")
            # TODO: 如果用户是队长，还应当读取战队邮箱
            if self.crt_user.is_leader:
                self.crt_team = self.crt_user.belong
                self.join_request = JoinRequest.objects.filter(send_to=self.crt_team). \
                    values("title", "content", "send_by", "send_time", "is_read", "agree")
            self.data = {
                # TODO: 如果 value 是 send_by，读取出用户名
                "normal_mail": [{k: (v.username if k == "send_by" else v)
                                 for k, v in item.items() } for item in self.normal_mail],
                "join_request": [{k: (User.objects.get(id=v).username if k == "send_by" else v)
                                  for k, v in item.items() } for item in self.join_request],
            }
            return 0
        except Exception as e:
            self.error = "query error:" + str(e)
            return 1

    def get(self, request):
        if not request.user.is_authenticated:
            self.code = 401
        else:
            self.crt_user = request.user
            self.code = self.get_mail()
        return JsonResponseZh(self.get_ret_code())

    def post(self, request):
        self.code = 10
        return JsonResponseZh(self.get_ret_code())