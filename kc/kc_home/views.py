from django.shortcuts import render


context = {'active': 'home'}


def home(request):
    return render(request, 'kc_home/home.html', context)


def proxy(request):
    return render(request, 'kc_home/proxy.html', context)