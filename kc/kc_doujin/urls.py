from django.conf.urls import patterns, url
from kc_doujin.views import KcComicList


urlpatterns = patterns('',
    url(r'^$', KcComicList.as_view(), name='kc-doujin'),
    url(r'^upload/$', 'kc_doujin.views.upload', name='kc-doujin-upload'),
    url(r'^upload/receiver/', 'kc_doujin.views.upload_receiver', name='kc-doujin-upload-receiver'),
    url(r'^publish/$', 'kc_doujin.views.publish', name='kc-doujin-publish'),
    url(r'^publish/uf(?P<fid>\d+)/$', 'kc_doujin.views.publish_uploaded_file', name='kc-doujin-publish-uploaded-file'),
    url(r'^delete/uf(?P<fid>\d+)/$', 'kc_doujin.views.delete_uploaded_file', name='kc-doujin-delete-uploaded-file'),
    url(r'^edit/cm(?P<cid>\d+)/$', 'kc_doujin.views.edit_comic', name='kc-doujin-edit-comic'),
    url(r'^delete/cm(?P<cid>\d+)/$', 'kc_doujin.views.delete_comic', name='kc-doujin-delete-comic'),
)