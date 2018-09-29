from django.shortcuts import render


# Create your views here.
def major_page(request):
    return render(request, 'major_page/index.html')

