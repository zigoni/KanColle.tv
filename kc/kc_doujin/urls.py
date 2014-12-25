from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^upload/$', 'kc_doujin.views.upload', name='kc-donjin-upload'),
    url(r'^upload/receiver/', 'kc_doujin.views.upload_receiver', name='kc-donjin-upload-receiver'),
    url(r'^publish/$', 'kc_doujin.views.publish', name='kc-donjin-publish'),
    url(r'^publish/uf(?P<fid>\d+)/$', 'kc_doujin.views.publish_uploaded_file', name='kc-donjin-publish-uploaded-file'),
    url(r'^delete/uf(?P<fid>\d+)/$', 'kc_doujin.views.delete_uploaded_file', name='kc-donjin-delete-uploaded-file'),
    url(r'^edit/cm(?P<cid>\d+)/$', 'kc_doujin.views.edit_comic', name='kc-donjin-edit-comic'),
    url(r'^delete/cm(?P<cid>\d+)/$', 'kc_doujin.views.delete_comic', name='kc-donjin-delete-comic'),
)