import re
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


class Password(View):
    code = password = username = None
    error_msg = {
        "length_error": "密码长度应该大于八个字符",
        "digit_error": "密码中至少应该包含一个数字",
        "upper_error": "密码中至少应该包含一个大写字母",
        "lower_error": "密码中至少应该包含一个小写字母",
        "symbol_error": "密码中至少应该包含一个特殊字符",
        "name_similar": "用户名密码过于相似",
    }
    result = {
        "length_error": True, "digit_error": True, "upper_error": True,
        "lower_error": True, "symbol_error": True, "name_similar": True,
    }

    def get_code(self):
        return {
            0: {"code": 0, "msg": "密码合法"},
            1: {"code": 1, "msg": "密码不合法",
                "data": {k: v for k, v in self.error_msg.items() if self.result[k]}
                },
            10: {"code": 10, "msg": "检测到攻击"}
        }[self.code]

    def check(self):
        self.result["length_error"] = len(self.password) < 8  # TODO: calculating the length
        self.result["digit_error"] = re.search(r"\d", self.password) is None  # TODO: searching for digits
        self.result["upper_error"] = re.search(r"[A-Z]", self.password) is None  # TODO: searching for uppercase
        self.result["lower_error"] = re.search(r"[a-z]", self.password) is None  # TODO: searching for lowercase
        self.result["symbol_error"] = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', self.password) is None  # TODO: searching for symbols
        self.result["name_similar"] = re.search(self.username, self.password) is not None  # TODO: searching for username
        # TODO: overall result
        self.code = 0 if not (self.result["length_error"] or self.result["digit_error"]
                              or self.result["upper_error"] or self.result["lower_error"]
                              or self.result["symbol_error"] or self.result["name_similar"]) else 1

    def post(self, request):
        self.username = request.POST.get("username")
        self.password = request.POST.get("password")
        self.check()
        return JsonResponseZh(self.get_code())

    def get(self, request):
        self.code = 10
        return JsonResponseZh(self.get_code())

    
