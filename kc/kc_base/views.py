from django.shortcuts import render


def view404(request):
    return render(request, '404.html', status=404)


def view500(request):
    return render(request, '500.html', status=500)