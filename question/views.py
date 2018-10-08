from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Question, Solve


def JsonResponseZh(json_data):
    """
    因为返回含中文的 Json 数据总是需要设置 {'ensure_ascii': False}，所以直接在此集成
    :param json_data: 需要返回的数据
    """
    return JsonResponse(json_data, json_dumps_params={'ensure_ascii': False})


# Create your views here.
class QuestionList(View):
    q_tag = q_list = data = code = None

    def get_ret_dict(self):
        return {
            0: {"code": 0, "msg": "题目列表查询成功",
                "data": self.data},
            1: {"code": 1, "msg": "题目列表为空"},
            2: {"code": 2, "msg": "请提供 question_tag 参数供查询"},
            10: {"code": 10, "msg": "检测到攻击"},
        }[self.code]

    def query_by_tag(self):
        self.q_list = Question.objects.filter(question_tag=self.q_tag)
        self.data = [{
            "question_id": question.id,
            "question_name": question.question_name,
            "score": question.score,
            "solved_by": question.solve_by.all().count(),
            "first_solved": getattr(getattr(Solve.objects.filter(which_question=question).order_by("time").first(),
                                            'who_solve',None), 'username', 'NOBODY')
        } for question in self.q_list]
        return 1 if self.data == [] else 0

    def get(self, request):
        self.q_tag = request.GET.get("question_tag")
        self.code = self.query_by_tag() if self.q_tag is not None else 2
        return JsonResponseZh(self.get_ret_dict())

    def post(self, request):
        self.code = 10
        return JsonResponseZh(self.get_ret_dict())


class QuestionMessage(View):
    q_id = q_info = code = data = None

    def get_ret_dict(self):
        return {
            0: {"code": 0, "msg": "题目信息查询成功",
                "data": self.data},
            1: {"code": 1, "msg": "该题目不存在"},
            2: {"code": 2, "msg": "请提供 question_name 参数供查询"},
            10: {"code": 10, "msg": "检测到攻击"},
            401: {"code": 401, "msg": "未授权用户"},
        }[self.code]

    def query_by_name(self):
        try:
            self.q_info = Question.objects.get(id=self.q_id)
            self.data = {
                "question_id": self.q_info.id,
                "question_name": self.q_info.question_name,
                "description": self.q_info.description,
                "annex_link": self.q_info.link,
                "question_score": self.q_info.score,
                "first_three_solved": [v.who_solve.username for k, v in
                                       enumerate(Solve.objects.filter(which_question=self.q_info)) if k < 3]
            }
            return 0
        except Question.DoesNotExist:
            return 1

    def get(self, request):
        if not request.user.is_authenticated:
            self.code = 401
            return JsonResponseZh(self.get_ret_dict())
        self.q_id = request.GET.get("question_id")
        self.code = self.query_by_name() if self.q_id is not None else 2
        return JsonResponseZh(self.get_ret_dict())

    def post(self, request):
        self.code = 10
        return JsonResponseZh(self.get_ret_dict())


@method_decorator(csrf_exempt, name="dispatch")
class CheckFlag(View):
    crt_user = q_id = q_flag = q_obj = code = None

    ret_dict = {
        0: {"code": 0, "msg": "提交 Flag 成功"},
        1: {"code": 1, "msg": "参数错误", "error": "提交 Flag 错误"},
        2: {"code": 1, "msg": "参数错误", "error": "请提供 question_id 参数供查询"},
        3: {"code": 1, "msg": "参数错误", "error": "请提交 flag"},
        4: {"code": 1, "msg": "参数错误", "error": "请求题目不存在"},
        5: {"code": 1, "msg": "参数错误", "error": "您已经解答过该题目"},
        10: {"code": 10, "msg": "检测到攻击"},
        401: {"code": 401, "msg": "未授权用户"},
    }

    def check(self):
        try:
            self.q_obj = Question.objects.get(id=self.q_id)
        except Question.DoesNotExist:
            return 4
        try:
            Solve.objects.get(who_solve=self.crt_user, which_question=self.q_obj)
            return 5
        except Solve.DoesNotExist:
            pass
        if not self.q_obj.check_flag(self.q_flag):
            return 1
        # TODO: 给当前用户添加 Score 并且建立 Solve 对象
        self.crt_user.score = self.crt_user.score + self.q_obj.score
        self.crt_user.save()
        u_s_q = Solve.objects.create(who_solve=self.crt_user,
                                     which_question=self.q_obj)
        u_s_q.save()
        return 0

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponseZh(self.ret_dict[401])
        self.q_id = request.POST.get("question_id")
        self.q_flag = request.POST.get("flag")
        self.crt_user = request.user
        print(self.q_id, self.q_flag)

        self.code = (self.check() if self.q_flag is not None else 3)\
            if self.q_id is not None else 2
        return JsonResponseZh(self.ret_dict[self.code])

    def get(self, request):
        return JsonResponseZh(self.ret_dict[10])
