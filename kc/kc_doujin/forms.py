#coding: utf-8

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class KcComicPublishForm(forms.Form):
    title = forms.CharField(label='标题', max_length=128)
    is_r18 = forms.BooleanField(label='绅士向', required=False, help_text='R18漫画请务必勾选此项')
    translator = forms.CharField(label='汉化组', required=False, max_length=24)
    description = forms.CharField(label='简介(不超过255字)', max_length=255, required=False, widget=forms.Textarea)

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.add_input(Submit('submit', '发布'))
        return helper