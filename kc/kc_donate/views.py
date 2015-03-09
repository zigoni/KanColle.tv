from django.shortcuts import render


context = {'active': 'donate'}


def home(request):
    return render(request, 'kc_donate/home.html', context)
