from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'presentation.views.views',
    url(r'^$', 'view_homepage', name='view_homepage'),
)

urlpatterns += patterns(
    'presentation.views.publication_views',
    url(r'^publication/view/$', 'view_publication', name='view_publication'),
    url(r'^publication/read/$', 'read_publication', name='read_publication'),
)

urlpatterns += patterns(
    'presentation.views.user.views',
    url(r'^profile/id/(?P<user_uid>\w+)/$', 'view_user_profile_by_id', name='view_user_profile_by_id'),
    url(r'^profile/(?P<url_name>\w+)/$', 'view_user_profile_by_url_name', name='view_user_profile_by_url_name'),
    url(r'^my/shelves/$', 'view_my_shelves', name='view_my_shelves'),
)

urlpatterns += patterns(
    'presentation.views.user.works_views',
    url(r'^my/works/$', 'view_my_works', name='view_my_works'),
    url(r'^my/works/writing/$', 'write_my_work', name='write_my_work'),
    url(r'^my/works/publishing/$', 'publish_my_work', name='publish_my_work'),
)

urlpatterns += patterns(
    'presentation.views.user.messages_views',
    url(r'^my/messages/$', 'view_my_messages', name='view_my_messages'),
)

urlpatterns += patterns(
    'presentation.views.user.transaction_views',
    url(r'^my/transaction/$', 'view_my_transaction', name='view_my_transaction'),
)

urlpatterns += patterns(
    'presentation.views.user.settings_views',
    url(r'^my/settings/profile/$', 'view_my_settings_profile', name='view_my_settings_profile'),
    url(r'^my/settings/account/$', 'view_my_settings_account', name='view_my_settings_account'),
)