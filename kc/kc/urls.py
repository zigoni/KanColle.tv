from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'kc_home.views.home', name='kc-home'),
    url(r'^connector/$', 'kc_connector.views.home', name='kc-connector'),
    url(r'^proxy/$', 'kc_home.views.proxy', name='kc-proxy'),
    url(r'^hosts/$', 'kc_home.views.hosts', name='kc-hosts'),
    url(r'^user/', include('kc_user.urls')),
)
