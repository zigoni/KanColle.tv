#coding: utf-8

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class KcComicUploadForm(forms.Form):
    file = forms.FileField(label='上传文件', help_text='只支持没有密码的RAR文件，文件大小不超过200M')

    error_messages = {
        'invalid_file_format': '文件不是RAR格式'
    }

    def clear_file(self):
        file = self.cleaned_data['file']
        ext = file.name[-3:].lower()
        if ext is not 'rar':
            raise forms.ValidationError(self.error_messages['invalid_file_format'])
        return file

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.add_input(Submit('submit', '上传'))
        return helper