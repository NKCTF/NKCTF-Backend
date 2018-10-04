from django.http import JsonResponse
from django.views import View
from user.models import User, Team


def JsonResponseZh(json_data):
    """
    因为返回含中文的 Json 数据总是需要设置 {'ensure_ascii': False}，所以直接在此集成
    :param json_data: 需要返回的数据
    """
    return JsonResponse(json_data, json_dumps_params={'ensure_ascii': False})


class SearchUser(View):
    code = data = search_for = target = None

    def get_ret_dict(self):
        return {
            0: {"code": 0, "msg": "获取信息成功",
                "data": self.data},
            1: {"code": 1, "msg": "用户不存在"},
            2: {"code": 2, "msg": "请提供一个用户名"},
            10: {"code": 10, "msg": "检测到攻击"},
            401: {"code": 401, "msg": "未授权用户"},
        }[self.code]

    def search_user_msg(self):
        try:
            self.target = User.objects.get(username=self.search_for)
            self.data = {
                "username": self.target.username,
                "email": self.target.email,
                "score": self.target.score,
                "qq": self.target.qq,
                "github": self.target.github,
                "description": self.target.description,
            }
            return 0
        except User.DoesNotExist:
            return 1

    def get(self, request):
        if not request.user.is_authenticated:
            self.code = 401
            return JsonResponseZh(self.get_ret_dict())
        self.search_for = request.GET.get("username")
        self.code = self.search_user_msg() if self.search_for is not None else 2
        return JsonResponseZh(self.get_ret_dict())

    def post(self):
        self.code = 10
        return JsonResponseZh(self.get_ret_dict())


class SearchTeam(View):
    code = data = search_for = team_obj = None

    def get_ret_dict(self):
        return {
            0: {"code": 0, "msg": "获取信息成功",
                "data": self.data},
            1: {"code": 1, "msg": "战队不存在"},
            2: {"code": 2, "msg": "请提供一个战队名"},
            10: {"code": 10, "msg": "检测到攻击"},
            401: {"code": 401, "msg": "未授权用户"},
        }[self.code]

    def query_team_msg(self):
        try:
            self.team_obj = Team.objects.get(team_name=self.search_for)
            query_leader = User.objects.filter(belong=self.team_obj, is_leader=True)
            self.data = {
                "team_name": self.team_obj.team_name,
                "team_description": self.team_obj.description,
                "members": len(User.objects.filter(belong=self.team_obj)),
                "leader": ' & '.join([it.username for it in query_leader]),
                "score": sum([it.score for it in User.objects.filter(belong=self.team_obj)]),
            }
            return 0
        except Team.DoesNotExist:
            return 1

    def get(self, request):
        if not request.user.is_authenticated:
            self.code = 401
            return JsonResponseZh(self.get_ret_dict())
        self.search_for = request.GET.get("team_name")
        self.code = self.query_team_msg() if self.search_for is not None else 2
        return JsonResponseZh(self.get_ret_dict())

    def post(self, request):
        self.code = 10
        return JsonResponseZh(self.get_ret_dict())

