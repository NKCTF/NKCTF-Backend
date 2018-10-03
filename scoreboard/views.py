import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth.decorators import login_required
from user.models import User, Team, Career
from django.db.models import F, FloatField, Sum


def JsonResponseZh(json_data):
    """
    因为返回含中文的 Json 数据总是需要设置 {'ensure_ascii': False}，所以直接在此集成
    :param json_data: 需要返回的数据
    """
    return JsonResponse(json_data, json_dumps_params={'ensure_ascii': False})


# Create your views here.
@login_required
@csrf_exempt
def user_score(request):
    # TODO: u_board 是一个 QuerySet 类型的数据，其类似于一个 list
    u_board = User.objects.all().order_by(F("score").desc()).values("username", "score", "qq", "user_career", "belong")
    # TODO; key 即列表的键，value 即为一个 query 出来的字典
    data = [{k: (Team.objects.get(id=v).team_name  # TODO: 将战队的 id 替换成为 name 指示战队名称
            if k == "belong" else v) for k, v in value.items()}
            for key, value in enumerate(u_board) if key < 10]  # TODO: if 条件决定返回数据量小于十个

    if data is not None:
        response_data = {
            'code': 0,
            'msg': "用户排名",
            'data': data,
        }
    else:
        response_data = {
            'code': 1,
            'msg': "用户排名查询失败",
        }
    return JsonResponseZh(response_data)


@login_required
@csrf_exempt
def team_score(request):
    t_board = User.objects.values_list('belong').aggregate(sum('score')).order_by(sum('score'))
    data = serializers.serialize('json', t_board)
    if t_board is not None:
        response_data = {
            'code': 0,
            'msg': "战队排名",
            'data': data,
        }
    else:
        response_data = {
            'code': 1,
            'msg': "战队排名查询失败",
        }
    return JsonResponse(response_data)
