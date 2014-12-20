#coding: utf-8

from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


UserModel = get_user_model()


class SignupForm(forms.ModelForm):
    password = forms.CharField(label='密码', max_length=128, widget=forms.PasswordInput)
    confirmed_password = forms.CharField(label='确认密码', max_length=128, widget=forms.PasswordInput)

    error_messages = {
        'duplicate_email': '电子邮件已被使用',
        'duplicate_username': '用户名已被使用',
        'password_mismatch': '两次输入的密码不匹配',
    }

    class Meta:
        model = UserModel
        fields = ['email', 'username', 'password', 'confirmed_password']

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.add_input(Submit('submit', '注册'))
        return helper

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password(self):
        return self.cleaned_data['password']

    def clean_confirmed_password(self):
        password = self.cleaned_data['password']
        confirmed_password = self.cleaned_data['confirmed_password']
        if password == confirmed_password:
            return confirmed_password
        else:
            raise forms.ValidationError(self.error_messages['password_mismatch'])


class ChangePasswordForm(forms.Form):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    old_password = forms.CharField(label='旧密码', max_length=128, widget=forms.PasswordInput)
    new_password = forms.CharField(label='新密码', max_length=128, widget=forms.PasswordInput)
    confirmed_password = forms.CharField(label='确认密码', max_length=128, widget=forms.PasswordInput)

    error_messages = {
        'invalid_old_password': '旧密码错误',
        'password_mismatch': '两次输入的密码不匹配',
    }

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if self.request.user.check_password(old_password):
            return old_password
        raise forms.ValidationError(self.error_messages['invalid_old_password'])

    def clean_confirmed_password(self):
        new_password = self.cleaned_data['new_password']
        confirmed_password = self.cleaned_data['confirmed_password']
        if new_password == confirmed_password:
            return confirmed_password
        else:
            raise forms.ValidationError(self.error_messages['password_mismatch'])

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.add_input(Submit('submit', '修改'))
        return helper


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(label='注册时使用的电子邮件：')

    error_messages = {
        'invalid_email': '没有用户使用此电子邮件注册',
    }

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            UserModel.objects.get(email=email)
            return email
        except UserModel.DoesNotExist:
            raise forms.ValidationError(self.error_messages['invalid_email'])

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.add_input(Submit('submit', '提交'))
        return helper


class ResetPasswordForm(forms.Form):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    new_password = forms.CharField(label='新密码', max_length=128, widget=forms.PasswordInput)
    confirmed_password = forms.CharField(label='确认新密码', max_length=128, widget=forms.PasswordInput)

    error_messages = {
        'password_mismatch': '两次输入的密码不匹配',
    }

    def clean_confirmed_password(self):
        new_password = self.cleaned_data['new_password']
        confirmed_password = self.cleaned_data['confirmed_password']
        if new_password == confirmed_password:
            return confirmed_password
        else:
            raise forms.ValidationError(self.error_messages['password_mismatch'])

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.add_input(Submit('submit', '提交'))
        return helper