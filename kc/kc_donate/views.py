from django.shortcuts import render
from kc_donate.models import KcDonateRecord

context = {'active': 'donate'}


def home(request):
    q = KcDonateRecord.objects.order_by('-donate_time')
    context['q'] = q
    return render(request, 'kc_donate/home.html', context)
