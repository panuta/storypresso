from django.conf import settings
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'accounts.views',

    url(r'^login/$', 'view_login', name='view_login'),
    url(r'^signup/$', 'view_signup', name='view_signup'),
)

urlpatterns += patterns('',
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}, name='auth_logout'),
    url(r'^accounts/password_reset/$', 'django.contrib.auth.views.password_reset', {'from_email':settings.NOREPLY_EMAIL}, name='auth_password_reset'),
    url(r'^accounts/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='auth_password_reset_done'),
    url(r'^accounts/reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm', name='auth_password_reset_confirm'),
    url(r'^accounts/reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='auth_password_reset_complete'),
)