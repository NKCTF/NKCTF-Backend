import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from user.models import User, Team
from django.db.models import F, FloatField, Sum

from django.core.serializers.json import DjangoJSONEncoder


def JsonResponseZh(json_data):
    """
    因为返回含中文的 Json 数据总是需要设置 {'ensure_ascii': False}，所以直接在此集成
    :param json_data: 需要返回的数据
    """
    return JsonResponse(json_data, json_dumps_params={'ensure_ascii': False})


# Create your views here.
# @login_required
@csrf_exempt
def user_score(request):
    u_board = User.objects.all().order_by("Score").values()
    # data = {key: values for key, values in enumerate(u_board)}
    # data = list(u_board)
    data = json.dumps(u_board, cls=DjangoJSONEncoder)
    print(data)
    if u_board is not None:
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


# @login_required
@csrf_exempt
def team_score(request):
    t_board = User.objects.values_list('Belong').aggregate(sum('Score')).order_by(sum('Score'))
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

