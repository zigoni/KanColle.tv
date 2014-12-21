#coding: utf-8

from django.db import models
from django.conf import settings


class KcUploadedComicFile(models.Model):
    file_name = models.CharField('文件名', max_length=200, unique=True, help_text='上传文件的完整文件名')
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='上传者', related_name='upload_files')
    upload_time = models.DateTimeField('上传时间', auto_now_add=True)


class KcComic(models.Model):
    title = models.CharField('标题', max_length=128)
    is_r18 = models.BooleanField('绅士向', default=False)
    is_active = models.BooleanField('是否可见', default=True)
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='发布者')
    publish_time = models.DateTimeField('发布时间', auto_now_add=True)
    translator = models.CharField('汉化组', blank=True, max_length=24)
    description = models.CharField('简介(不超过255字)', max_length=255)
    file = models.OneToOneField(KcUploadedComicFile, related_name='comic')
    pages = models.PositiveIntegerField('页码数', default=0)