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
    return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})


def is_valid_username(username):
    if 2 < len(username) < 16:
        return True
    return False


@csrf_exempt
def user_signup(request):
    if request.method == "GET" and request.GET.get("username") is not None:
        user_name = request.GET.get("username")
        if not is_valid_username(user_name):
            response_data = {
                'code': 1,
                'msg': "用户名不合法",
            }
        else:
            try:
                User.objects.get(username=user_name)
                response_data = {
                    'code': 2,
                    'msg': "用户名已存在",
                }
            except User.DoesNotExist:
                response_data = {
                    'code': 0,
                    'msg': "好的",
                }
    elif request.method == "POST":
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
    else:
        response_data = {
            'code': 10,
            'msg': "检测到攻击",
        }
    return JsonResponse(response_data, json_dumps_params={'ensure_ascii':False})
