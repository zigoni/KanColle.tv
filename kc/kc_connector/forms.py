#coding: utf-8

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class DmmLoginForm(forms.Form):
    login_id = forms.EmailField(label='DMM登录ID', max_length=30, required=True,
                                error_messages={'required': '请输入电子邮件', 'invalid': '请输入格式正确的电子邮件'})
    password = forms.CharField(label='DMM登录密码', max_length=30, required=True, widget=forms.PasswordInput,
                               error_messages={'required': '请输入密码'})

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.add_input(Submit('submit', '登录游戏'))
        return helper
