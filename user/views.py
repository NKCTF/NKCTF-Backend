from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def user_login(request):
    print(request.method)
    if request.method != "POST":
        response_data = {
            'code': 10,
            'msg': "检测到攻击",
        }
    else:
        user_name = request.POST.get("username")
        pass_word = request.POST.get("password")
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            response_data = {
                'code': 0,
                'msg': "登录成功",
            }
        else:
            response_data = {
                'code': 1,
                'msg': "用户名或密码错误",
            }
    return JsonResponse(response_data, json_dumps_params={'ensure_ascii':False})


@csrf_exempt
def user_signup(request):
    if request.method != "POST":
        response_data = {
            'code': 10,
            'msg': "检测到攻击",
        }
    else:
        user_name = request.POST.get("username")
        pass_word = request.POST.get("password")
        try:
            User.objects.get(username=user_name)
            response_data = {
                'code': 2,
                'msg': "用户名已存在",
            }
        except User.DoesNotExist:
            print(user_name)
            newer = User.objects.create(username=user_name)
            newer.set_password(pass_word)
            newer.save()
            response_data = {
                'code': 0,
                'msg': "注册成功",
            }
    return JsonResponse(response_data, json_dumps_params={'ensure_ascii':False})
