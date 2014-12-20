import hashlib
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from kc_user.config import *
from kc_user.models import *
from kc_user.forms import *


context = {'active': 'user'}


@login_required
def home(request):
    return render(request, 'kc_user/home.html', context)


def signup(request):
    if KC_USER_SIGNUP:
        if request.user.is_authenticated():
            context['title'] = '已注册用户不能重复注册'
            context['message'] = '您已经是KanColle.tv的注册用户了，无需重新注册！'
            return render(request, 'warning.html', context)
        form = SignupForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = KcUser.objects.create_user(email=email, username=username, password=password)
            user.save()

            hashstr = email+username+password+KcUser.objects.make_random_password()
            email_confirmation_code = hashlib.md5(hashstr.encode('utf-8')).hexdigest()
            email_confirmation = KcUserEmailConfirmation.objects.create(user=user, code=email_confirmation_code)
            email_confirmation.save()

            mail_subject = 'KanColle.tv注册用户激活'
            mail_body = '%s，您好！\n感谢您注册成为KanColle.tv的用户，请用下面的链接激活您的账号：\n\nhttp://kancolle.tv/user/confirmation/%s/\n\n本邮件由系统自动发送，请勿回复' % (username, email_confirmation_code)
            mail_from = 'webmaster@kancolle.tv'
            mail_to = [email, ]
            send_mail(mail_subject, mail_body, mail_from, mail_to)

            context['title'] = '注册成功'
            context['message'] = '注册KanColle.tv用户成功，请查收您的邮箱以激活您的账号。'
            return render(request, 'message.html', context)
        context['form'] = form
        return render(request, 'kc_user/signup.html', context)
    else:
        context['title'] = '关闭注册'
        context['message'] = '本站暂不开放注册。'
        return render(request, 'message.html', context)


def confirmation(request, code):
    try:
        confirmation = KcUserEmailConfirmation.objects.get(code=code)
    except KcUserEmailConfirmation.DoesNotExist:
        context['title'] = '激活码无效'
        context['message'] = '激活码无效，激活失败！'
        return render(request, 'warning.html', context)
    user = confirmation.user
    user.is_active = True
    user.save(update_fields=['is_active'])
    confirmation.delete()
    context['title'] = '激活成功'
    context['message'] = '您的账号已激活成功，请从页面右上角的登录按钮登录。'
    return render(request, 'message.html', context)


@login_required
def changepassword(request):
    form = ChangePasswordForm(data=(request.POST or None), request=request)
    if form.is_valid():
        user = request.user
        user.set_password(form.cleaned_data['new_password'])
        request.user.save(update_fields=['password'])
        context['title'] = '修改密码成功'
        context['message'] = '修改密码成功！'
        return render(request, 'message.html', context)
    context['form'] = form
    return render(request, 'kc_user/changepassword.html', context)


def forgetpassword(request):
    pass


def resetpassword(request):
    pass