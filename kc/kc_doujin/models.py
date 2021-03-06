#coding: utf-8

import hashlib
from django.db import models
from django.conf import settings


class KcUploadedComicFile(models.Model):
    file_name = models.CharField('文件名', max_length=200, unique=True, help_text='上传文件的完整文件名')
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='上传者', related_name='upload_files')
    upload_time = models.DateTimeField('上传时间', auto_now_add=True)
    md5 = models.CharField('MD5哈希值', max_length=32, unique=True)
    linked = models.BooleanField('是否与漫画关联', default=False)

    def get_extract_dir(self):
        s = '%d_%s' % (self.pk, self.md5)
        return hashlib.md5(s.encode('utf-8')).hexdigest()

    class Meta:
        verbose_name = '已上传同人漫画文件'
        verbose_name_plural = '已上传同人漫画文件'

    def __str__(self):
        return self.file_name


class KcComic(models.Model):
    title = models.CharField('标题', max_length=128)
    is_r18 = models.BooleanField('绅士向', default=False)
    is_active = models.BooleanField('是否可见', default=True)
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='发布者')
    publish_time = models.DateTimeField('发布时间', auto_now_add=True)
    translator = models.CharField('汉化组', blank=True, max_length=24, default='')
    description = models.CharField('简介(不超过255字)', blank=True, max_length=255, default='')
    file = models.OneToOneField(KcUploadedComicFile, related_name='comic')
    pages = models.PositiveIntegerField('页码数', default=0)
    clicks = models.PositiveIntegerField('阅读次数', default=0)

    def get_img_prefix(self):
        return '%sdoujin/%s/' % (settings.MEDIA_URL, self.file.get_extract_dir())

    class Meta:
        verbose_name = '同人漫画'
        verbose_name_plural = '同人漫画'
        ordering = ['-publish_time']

    def __str__(self):
        return self.title