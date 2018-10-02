from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from random import choice as random_choice
from requests import post as send_post, get as send_get
from urllib.parse import quote as url_quote


def JsonResponseZh(json_data):
    """
    因为返回含中文的 Json 数据总是需要设置 {'ensure_ascii': False}，所以直接在此集成
    :param json_data: 需要返回的数据
    """
    return JsonResponse(json_data, json_dumps_params={'ensure_ascii': False})


# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class Login(View):
    code = {
        0: {"code": 0, "msg": "登录成功"},
        1: {"code": 1, "msg": "用户名或密码错误"},
        10: {"code": 10, "msg": "检测到攻击"},
    }

    def get(self, request):
        return JsonResponseZh(self.code[10])

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username)
        if user is not None and user.check_password(password):
            login(request, user)
            return JsonResponseZh(self.code[0])
        else:
            return JsonResponseZh(self.code[1])


# @method_decorator(csrf_exempt, name="dispatch")
# class AuthLogin(View):


@method_decorator(csrf_exempt, name="dispatch")
class Signup(View):
    code = {
        "get0": {"code": 0, "msg": "好的"},
        "post0": {"code": 0, "msg": "注册成功"},
        1: {"code": 1, "msg": "用户名不合法"},
        2: {"code": 2, "msg": "用户名已存在"},
        10: {"code": 10, "msg": "检测到攻击"},
    }
    name_range = [2, 16]

    def is_valid_username(self, username):
        return True if (self.name_range[0] < len(username) < self.name_range[1]) else False

    def get(self, request):
        """如果是 get 方式请求，会调用这个函数"""
        username = request.GET.get("username")
        if not self.is_valid_username(username):
            return JsonResponseZh(self.code[1])
        try:
            User.objects.get(username=username)
            return JsonResponseZh(self.code[2])
        except User.DoesNotExist:
            return JsonResponseZh(self.code["get0"])

    def post(self, request):
        """如果是 post 方式请求，会调用这个函数"""
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            User.objects.get(username=username)
            return JsonResponseZh(self.code[2])
        except User.DoesNotExist:
            newer = User.objects.create(username=username)
            newer.set_password(password)
            newer.save()
            return JsonResponseZh(self.code["get0"])


def user_auth_in(request):
    host = request.META.get('HTTP_HOST')
    message_type = request.GET.get('type')
    # TODO: generate a state
    state = 'safe_string'
    location_host = 'https://github.com/login/oauth/authorize'
    client_id = 'b7bc968987af28497e2d'
    redirect_uri = url_quote(f'http://{host}/user/auth_back?type={message_type}&state={state}&allow_signup=false')
    return HttpResponse(
        f'<script>' 
        f'  setTimeout(function(){{'
        f"    document.location = '{location_host}?client_id={client_id}&redirect_uri={redirect_uri}';"
        f'}}, 1000);'
        f'</script>')


@csrf_exempt
def user_auth_back(request):
    code = request.GET.get("code")
    host = request.META.get('HTTP_HOST')
    # TODO: consume the state, if not present, don't proceed
    state = request.GET.get("state")
    message_type = request.GET.get('type')

    post_data = {
        "client_id": "b7bc968987af28497e2d",
        "client_secret": "1347f0ae61ef050fbb0aafd83753a6cb677a0c1d",
        "code": code,
        "redirect_uri": f"http://{host}/user/auth_back",
        "state": state,
    }

    response = send_post("https://github.com/login/oauth/access_token/", json=post_data,
                         headers={'accept': 'application/json'})
    received_json_data = response.json()

    access_token = received_json_data.get("access_token")
    token_type = received_json_data.get("token_type")

    if access_token is None or token_type is None:
        print(received_json_data)
        error = received_json_data.get("error")
        return HttpResponse(
            f'<script>'
            f'  window.opener.postMessage({{'
            f'    type: "{message_type}",'
            f'    code: 1,'
            f'    error: {error} '
            f'  }}, "*"'
            f')'
            f'</script>')

    response = send_get("https://api.github.com/user", headers={
        'Accept': 'application/json',
        'Authorization': f'token {access_token}'
    })
    received_json_data = response.json()

    ghUsername = received_json_data.get('login')
    ghRealname = received_json_data.get('name')
    ghEmail = received_json_data.get('email')
    print(received_json_data)
    # User.objects.create(username=)
    data_str = f'{{ username: "{ghUsername}", email: "{ghEmail}" }}'
    return HttpResponse(
        f'<script>'
        f'  window.opener.postMessage({{'
        f'    type: "{message_type}",'
        f'    code: 0,'
        f'    data: {data_str} '
        f'  }}, "*"'
        f')'
        f'</script>')
