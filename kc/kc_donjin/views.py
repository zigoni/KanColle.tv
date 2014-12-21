from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from kc_donjin.forms import KcComicUploadForm
from kc_donjin.lib import handle_uploaded_file


context = {'active': 'donjin'}


@login_required
def upload(request):
    u = request.user
    if not (u.is_superuser or u.is_staff or u.is_donjin_publisher or u.is_donjin_uploader):
        context['title'] = '权限不足'
        context['message'] = '只有属于同人志上传组或发布组的用户才能进行本操作'
        return render(request, 'warning.html', context)

    form = KcComicUploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        path = handle_uploaded_file(request.FILES['file'])
        if path:
            context['success'] = True
        else:
            context['success'] = False
    else:
        pass
    context['form'] = form
    return render(request, 'kc_donjin/mgt_upload.html', context)