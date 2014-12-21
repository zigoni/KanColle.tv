#coding: utf-8

import re
from django.core import validators
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from kc_donjin.config import *


class KcUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, is_active=False, is_superuser=False, is_staff=False, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        user = self.create_user(email=email, username=username, password=password, **extra_fields)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class KcGroup(models.Model):
    symbol = models.CharField('标志', max_length=20, unique=True,
        help_text='用于系统内部识别的标志，必须以英文字母开头，之后可有英文字母、数字或下划线，长度不超过20',
        validators=[validators.RegexValidator(re.compile('^[\w][\w\d_]{0,19}$'), '请按格式输入', 'invalid')])
    name = models.CharField('名称', max_length=20, unique=True,
        help_text='用于显示的名称，可使用任意字符，HTML标记无效，长度不超过20')
    description = models.CharField('描述', max_length=200,
        help_text='对用户组的描述，可使用任意字符，HTML标记无效，长度不超过200')

    class Meta:
        verbose_name = '用户组'
        verbose_name_plural = '用户组'

    def __str__(self):
        return self.name


class KcUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('电子邮件', max_length=254, unique=True,
        help_text='电子邮件必须真实有效，否则将无法激活账号')
    username = models.CharField('用户昵称', max_length=20, unique=True, db_index=True,
        help_text='用户昵称可由英文字母、数字、汉字或假名组成，长度不超过20',
        validators=[
            validators.RegexValidator(re.compile('^[\\w\\d\u2e80-\u9fff]{2,}$'), '请输入至少两个字母、数字、汉字或假名', 'invalid')
        ])
    is_active = models.BooleanField('用户是否可用', default=True)
    is_staff = models.BooleanField('是否为管理用户', default=False)
    create_time = models.DateTimeField('用户创建时间', default=timezone.now)
    kc_groups = models.ManyToManyField(KcGroup, blank=True, verbose_name='所属用户组')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = KcUserManager()

    def get_full_name(self):
        full_name = '%s(%s)' % (self.username, self.email)
        return full_name

    def get_short_name(self):
        return self.username

    def get_kc_groups(self):
        kc_groups = set([g.symbol for g in self.kc_groups.all()])
        return kc_groups

    def is_donjin_uploader(self):
        kc_groups = self.get_kc_groups()
        if KC_DONJIN_UPLOADER in kc_groups:
            return True
        else:
            return False

    def is_donjin_publisher(self):
        kc_groups = self.get_kc_groups()
        if KC_DONJIN_PUBLISHER in kc_groups:
            return True
        else:
            return False

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.get_full_name()


class KcUserPasswordReset(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='password_reset')
    code = models.CharField('密码重置代码', max_length=32)
    create_time = models.DateTimeField('密码重置请求创建时间', default=timezone.now)

    class Meta:
        verbose_name = '密码重置请求'
        verbose_name_plural = '密码重置请求'

    def __str__(self):
        return '%s 的密码重置请求' % self.user.get_full_name()


class KcUserEmailConfirmation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='email_confirmation')
    code = models.CharField('电子邮件确认代码', max_length=32)
    create_time = models.DateTimeField('电子邮件确认请求创建时间', default=timezone.now)

    class Meta:
        verbose_name = '电子邮件确认请求'
        verbose_name_plural = '电子邮件确认请求'

    def __str__(self):
        return '%s 的电子邮件确认请求' % self.user.get_full_name()