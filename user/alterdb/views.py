from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View


def JsonResponseZh(json_data):
    """
    因为返回含中文的 Json 数据总是需要设置 {'ensure_ascii': False}，所以直接在此集成
    :param json_data: 需要返回的数据
    """
    return JsonResponse(json_data, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class AlterPersonal(View):
    code = data = error = crt_user = None
    target_attr = new_value = None
    allow_attr = ["username", "description", "email", "qq", "github"]

    def get_ret_dict(self):
        return {
            0: {"code": 0, "msg": "获取信息成功",
                "data": self.data},
            1: {"code": 1, "msg": "请指定更改对象与新值"},
            2: {"code": 2, "msg": "不允许更改字段或不存在字段"},
            3: {"code": 3, "msg": "更改数据库错误",
                "error": self.error},
            10: {"code": 10, "msg": "检测到攻击"},
            401: {"code": 401, "msg": "未授权用户"},
        }[self.code]

    def set_user_msg(self):
        try:
            if self.target_attr not in self.allow_attr:
                return 2
            setattr(self.crt_user, self.target_attr, self.new_value)
            self.ctr_user.save()
            return 0
        except Exception as e:
            self.error = str(e)
            return 3

    def get(self, request):
        print(request.method)
        self.code = 10
        return JsonResponseZh(self.get_ret_dict())

    def post(self, request):
        if not request.user.is_authenticated:
            self.code = 401
            return JsonResponseZh(self.get_ret_dict())
        self.crt_user = request.user
        self.target_attr = request.POST.get("attribute")
        self.new_value = request.POST.get("value")
        self.code = self.set_user_msg() if (self.target_attr is not None
                                            and self.new_value is not None) else 1
        return JsonResponseZh(self.get_ret_dict())


