from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    #url(r'^$', 'kc_user.views.home', name='account-home'),
    url(r'^signup/$', 'kc_user.views.signup', name='user-signup'),
    url(r'^login/$', login, {'template_name': 'kc_user/login.html', 'extra_context': {'active': 'user'}}, name='user-login'),
    url(r'^logout/$', logout, {'template_name': 'kc_user/logout.html'}, name='user-logout'),
    url(r'^confirmation/(?P<code>\w+)/$', 'kc_user.views.confirmation', name='user-email-confirmation'),
    #url(r'^changepassword/$', 'kc_user.views.changepassword', name='user-change-password'),
    url(r'^forgetpassword/$', 'kc_user.views.forgetpassword', name='user-forget-password'),
    #url(r'^resetpassword/(?P<code>\w+)/$', 'kc_user.views.resetpassword', name='account-reset-password'),
)