from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers


# Create your views here.
@csrf_exempt
def question_lst(request):
    print(request.method)
    from question import models
    question_list = models.Question.objects.all()
    data = serializers.serialize('json', question_list)
    if question_list is not None:
        response_data = {
            'code': 0,
            'msg': "题目列表",
            'data': data,
        }
    else:
        response_data = {
            'code': 1,
            'msg': "题目列表查询失败",
        }
    return JsonResponse(response_data)


def question_msg(request):
    from question import models
    print(request.method)
    if request.method != "POST":
        response_data = {
            'code': 10,
            'msg': "检测到攻击",
        }
    else:
        question_id = request.POST.get("questionid")
        question_message = models.Question.objects.get(id=question_id)
        data = {
            'PossibleTag': question_message.PossibleTag,
            'Tag': question_message.Tag,
            'Name': question_message.Name,
            'Description': question_message.Description,
            'Link': question_message.Link,
            'Score': question_message.Score
        }
        if question_message is not None:
            response_data = {
                'code': 0,
                'msg': "题目信息",
                'data': data,
            }
        else:
            response_data = {
                'code': 1,
                'msg': "题目信息查询失败",
            }
    return JsonResponse(response_data)


def question_flag(request):
    from question import models
    print(request.method)
    if request.method != "POST":
        response_data = {
            'code': 10,
            'msg': "检测到攻击",
        }
    else:
        question_flag = request.POST.get("flag")
        question_id = request.POST.get("questionid")
        flag = models.Question.objects.get(id=question_id)
        if question_flag == flag:
            response_data = {
                'code': 0,
                'msg': "题目列表",
                'data': "Flag 正确",
            }
        else:
            response_data = {
                'code': 3,
                'msg': "Flag 错误",
            }
    return JsonResponse(response_data)
