from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'kc_donate.views.home', name='kc-donate'),
)
