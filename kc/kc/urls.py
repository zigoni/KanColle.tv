from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'kc_home.views.home', name='kc-home'),
    url(r'^connector/$', 'kc_connector.views.home', name='kc-connector'),
    url(r'^proxy/$', 'kc_home.views.proxy', name='kc-proxy'),
    url(r'^hosts/$', 'kc_home.views.hosts', name='kc-hosts'),
    url(r'^user/', include('kc_user.urls')),
    url(r'^doujin/', include('kc_doujin.urls')),
    url(r'^donate/', include('kc_donate.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

handler404 = 'kc_base.views.view404'
handler500 = 'kc_base.views.view500'