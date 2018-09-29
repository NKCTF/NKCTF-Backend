from django.shortcuts import render


# Create your views here.
def login_page(request):
    if request.method != "POST":
        return render(request, 'start_page/index.html', {"isLogin": False})

    if request.POST['user_name'] == 'root' and request.POST['password'] == 'root':
        return render(request, 'major_page/index.html')
    else:
        return render(request, "start_page/index.html", {"isLogin": True})
