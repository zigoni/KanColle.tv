from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^upload/$', 'kc_donjin.views.upload', name='kc-donjin-upload'),
)