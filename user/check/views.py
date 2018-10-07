import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from user.models import User, Team


def JsonResponseZh(json_data):
    """
    因为返回含中文的 Json 数据总是需要设置 {'ensure_ascii': False}，所以直接在此集成
    :param json_data: 需要返回的数据
    """
    return JsonResponse(json_data, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
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

    def get_ret_dict(self):
        return {
            0: {"code": 0, "msg": "密码合法"},
            1: {"code": 1, "msg": "密码不合法",
                "error": " & ".join([v for k, v in self.error_msg.items() if self.result[k]])},
            2: {"code": 2, "msg": "请传递密码参数"},
            10: {"code": 10, "msg": "检测到攻击"},
        }[self.code]

    def check(self):
        self.result["length_error"] = len(self.password) < 8  # TODO: calculating the length
        self.result["digit_error"] = re.search(r"\d", self.password) is None  # TODO: searching for digits
        self.result["upper_error"] = re.search(r"[A-Z]", self.password) is None  # TODO: searching for uppercase
        self.result["lower_error"] = re.search(r"[a-z]", self.password) is None  # TODO: searching for lowercase
        self.result["symbol_error"] = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', self.password) is None  # TODO: searching for symbols
        if self.username is not None:
            # TODO: searching for username
            self.result["name_similar"] = re.search(self.username, self.password) is not None
        else:
            print("Username similarity doesn't check.")
            self.result["name_similar"] = False
        # TODO: 如果 result 中的所有值为 False, code = 0, 否则为 1
        return 0 if ([v for v in self.result.values() if v] == []) else 1

    def post(self, request):
        self.username = request.POST.get("username")
        self.password = request.POST.get("password")
        self.code = self.check() if self.password is not None else 2
        return JsonResponseZh(self.get_ret_dict())

    def get(self, request):
        self.code = 10
        return JsonResponseZh(self.get_ret_dict())


class Username(View):
    username = code = None
    banned_username = ["root", "admin", "superuser", "NOBODY"]
    error_msg = {
        "length_out_range": "用户名应该在 6 到 18 个字符之内",
        "user_exist": "用户名已存在",
        "is_reserved": "请勿使用保留用户名注册",
    }
    result = {
        "length_out_range": True,
        "user_exist": True,
        "is_reserved": True,
    }

    def get_ret_dict(self):
        return {
            0: {"code": 0, "msg": "用户名合法"},
            1: {"code": 1, "msg": "用户名不合法",
                "error": " & ".join([v for k, v in self.error_msg.items() if self.result[k]])},
            10: {"code": 10, "msg": "检测到攻击"},
        }[self.code]

    def check(self):
        self.result["length_out_range"] = len(self.username) not in range(6, 18)  # TODO: 检查用户名长度是否在 6-18 之间
        try:
            User.objects.get(username=self.username)
            self.result["user_exist"] = True
        except User.DoesNotExist:
            self.result["user_exist"] = False
        self.result["is_reserved"] = self.username in self.banned_username
        return 0 if ([v for v in self.result.values() if v] == []) else 1

    def post(self, request):
        self.code = 10
        return JsonResponseZh(self.get_ret_dict())

    def get(self, request):
        self.username = request.GET.get("username")
        self.code = self.check()
        return JsonResponseZh(self.get_ret_dict())


class TeamName(View):
    team_name = code = None
    banned_team_name = ["root", "admin", "superuser", "HAVEN'T JOIN YET."]
    error_msg = {
        "length_out_range": "战队应该在 6 到 18 个字符之内",
        "team_exist": "战队名已存在",
        "is_reserved": "请勿使用保留战队名注册",
    }
    result = {
        "length_out_range": True,
        "team_exist": True,
        "is_reserved": True,
    }

    def get_ret_dict(self):
        return {
            0: {"code": 0, "msg": "战队名合法"},
            1: {"code": 1, "msg": "战队名不合法",
                "error": " & ".join([v for k, v in self.error_msg.items() if self.result[k]])},
            10: {"code": 10, "msg": "检测到攻击"},
        }[self.code]

    def check(self):
        self.result["length_out_range"] = len(self.team_name) not in range(6, 18)  # TODO: 检查用户名长度是否在 6-18 之间
        try:
            Team.objects.get(team_name=self.team_name)
            self.result["team_exist"] = True
        except Team.DoesNotExist:
            self.result["team_exist"] = False
        self.result["is_reserved"] = self.team_name in self.banned_team_name
        return 0 if ([v for v in self.result.values() if v] == []) else 1

    def post(self, request):
        self.code = 10
        return JsonResponseZh(self.get_ret_dict())

    def get(self, request):
        self.team_name = request.GET.get("team_name")
        self.code = self.check()
        return JsonResponseZh(self.get_ret_dict())
