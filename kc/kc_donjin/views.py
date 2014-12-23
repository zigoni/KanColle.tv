import json
import hashlib
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from kc_donjin.lib import handle_uploaded_file
from kc_donjin.models import KcUploadedComicFile

context = {'active': 'donjin'}


@login_required
def upload(request):
    u = request.user
    if not (u.is_superuser or u.is_staff or u.is_donjin_publisher or u.is_donjin_uploader):
        context['title'] = '权限不足'
        context['message'] = '只有属于同人志上传组或发布组的用户才能进行本操作'
        return render(request, 'warning.html', context)

    context['extra_css'] = ('css/uploadfile.min.css', )
    context['extra_js'] = ('js/jquery.cookie.js', 'js/jquery.form.min.js', 'js/jquery.uploadfile.min.js', )
    return render(request, 'kc_donjin/mgt_upload.html', context)


@login_required
def upload_receiver(request):
    response = {
        'class': 'alert-danger',
        'message': '',
        'rar_file': '',
    }
    u = request.user
    if not (u.is_superuser or u.is_staff or u.is_donjin_publisher or u.is_donjin_uploader):
        response['message'] = '<p">您没有上传文件的权限。</p>'
    elif request.method != 'POST':
        response['message'] = '<p">请手下留情，不要攻击本站。</p>'
    elif request.FILES['rar_file']:
        path = handle_uploaded_file(request.FILES['rar_file'])
        if path:
            md5 = hashlib.md5(open(path, 'rb').read()).hexdigest()
            try:
                f = KcUploadedComicFile.objects.get(md5=md5)
            except KcUploadedComicFile.DoesNotExist:
                f = None
            if f is None:
                f = KcUploadedComicFile.objects.create(file_name=os.path.basename(path), uploader=u, md5=md5)
                f.save()
                response = {
                    'class': 'alert-success',
                    'message': '<p>文件上传成功！</p><p><a href="%s" class="alert-link">继续上传</a></p>' % reverse('kc-donjin-upload'),
                    'rar_file': path,
                }
            else:
                response['message'] = '<p">您上传的文件已经存在。</p><p><a href="%s" class="alert-link">重新上传</a></p>' % reverse('kc-donjin-upload')
        else:
            response['message'] = '<p">您上传的文件不符合系统要求。</p><p><a href="%s" class="alert-link">重新上传</a></p>' % reverse('kc-donjin-upload')
    else:
        response['message'] = '<p>你上传了什么鬼？</p>'
    return HttpResponse(json.dumps(response), content_type='text/plain')