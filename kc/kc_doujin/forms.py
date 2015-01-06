#coding: utf-8

import os
import logging
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from kc_doujin.config import KC_DOUJIN_UPLOAD_DIR


logger = logging.getLogger('django.request')


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


class KcUploadedComicFileEditForm(forms.Form):
    file_name = forms.CharField(label='文件名', max_length=128)

    error_messages = {
        'invalid_path': '文件名非法',
        'file_name_exists': '文件名与已有文件冲突',
    }

    def clean_file_name(self):
        file_name = self.cleaned_data['file_name']
        path = os.path.join(KC_DOUJIN_UPLOAD_DIR, file_name)
        base_dir = os.path.dirname(KC_DOUJIN_UPLOAD_DIR)
        upload_dir = os.path.dirname(os.path.abspath(path))
        logger.debug('%s, %s, %s' % (path, base_dir, upload_dir))
        if base_dir != upload_dir:
            raise forms.ValidationError(self.error_messages['invalid_path'])
        if os.path.exists(path):
            raise forms.ValidationError(self.error_messages['file_name_exists'])
        return file_name

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.add_input(Submit('submit', '修改'))
        return helper