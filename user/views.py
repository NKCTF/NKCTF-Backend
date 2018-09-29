import json
from django.http import HttpResponse
from django.contrib.auth import authenticate, login


# Create your views here.
def user_login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        response_data = {
            'code': 0,
            'msg': "登录成功",
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data = {
            'code': 1,
            'msg': "用户名或密码错误",
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
