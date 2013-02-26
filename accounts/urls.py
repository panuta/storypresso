from django.conf import settings
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    'accounts.views',
    url(r'^login/$', 'view_login', name='view_login'),
    url(r'^signup/$', 'view_signup', name='view_signup'),
    url(r'^signup/resend/$', 'view_signup_resend', name='view_signup_resend'),

    url(r'^login/facebook/$', 'login_facebook', name='login_facebook'),
    url(r'^accounts/error/$', TemplateView.as_view(template_name="accounts/registration/registration_login_error.html"), name='view_user_login_error'),
    url(r'^signup/done/$', 'view_user_signup_done', name='view_user_signup_done'),
    url(r'^activate/(?P<key>\w+)/$', 'activate_email_user', name='activate_email_user'),
    url(r'^accounts/redirect/$', 'login_facebook_redirect', name='login_facebook_redirect'),
)

urlpatterns += patterns('',
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}, name='auth_logout'),
    url(r'^accounts/password_reset/$', 'django.contrib.auth.views.password_reset', {'from_email':settings.EMAIL_MAILBOXES['bot']['address']}, name='auth_password_reset'),
    url(r'^accounts/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='auth_password_reset_done'),
    url(r'^accounts/reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm', name='auth_password_reset_confirm'),
    url(r'^accounts/reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='auth_password_reset_complete'),
)