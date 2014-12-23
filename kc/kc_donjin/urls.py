from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^upload/$', 'kc_donjin.views.upload', name='kc-donjin-upload'),
    url(r'^upload/receiver/', 'kc_donjin.views.upload_receiver', name='kc-donjin-upload-receiver')
)