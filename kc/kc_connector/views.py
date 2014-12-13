import requests.exceptions
from django.shortcuts import render
from kc_connector.connector import get_play_url
from kc_connector.forms import DmmLoginForm
from kc_connector.exceptions import *


context = {
    'active': 'connector',
}


def home(request):
    context['success'] = False
    context['message'] = ''
    context['play_url'] = ''
    form = DmmLoginForm(request.POST or None)
    if form.is_valid():
        login_id = form.cleaned_data['login_id']
        password = form.cleaned_data['password']
        try:
            context['play_url'] = get_play_url(login_id, password)
            context['success'] = True
            context['message'] = '登录DMM网站成功！'
        except DmmTokenError:
            context['message'] = '访问DMM网站失败！'
        except TokenError:
            context['message'] = '访问DMM网站失败！'
        except AjaxRequestError:
            context['message'] = '访问DMM网站失败！'
        except LoginError:
            context['message'] = '登录DMM网站失败！如果您没输错密码的话，可能是DMM强制要求您修改密码了。'
        except requests.exceptions.Timeout:
            context['message'] = '访问DMM网站超时！DMM可能遇到麻烦了……'
        except:
            context['message'] = '未知错误！'
    context['form'] = form
    return render(request, 'kc_connector/home.html', context)