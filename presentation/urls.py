from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'presentation.views.views',
    url(r'^$', 'view_homepage', name='view_homepage'),
)

urlpatterns += patterns(
    'presentation.views.story_views',
    url(r'^story/(?P<story_uid>[\w-]+)/view/$', 'view_story', name='view_story'),
    url(r'^story/(?P<story_uid>[\w-]+)/read/$', 'read_story', name='read_story'),
)

urlpatterns += patterns(
    'presentation.views.user.views',
    url(r'^profile/id/(?P<user_uid>\w+)/$', 'view_user_profile_by_id', name='view_user_profile_by_id'),
    url(r'^profile/(?P<url_name>\w+)/$', 'view_user_profile_by_url_name', name='view_user_profile_by_url_name'),
)

urlpatterns += patterns(
    'presentation.views.user.shelf_views',
    url(r'^my/shelves/$', 'view_my_shelves', name='view_my_shelves'),
)

urlpatterns += patterns(
    'presentation.views.user.stories_views',
    url(r'^my/stories/$', 'view_my_stories', {'showing_stories': 'all'}, name='view_my_stories'),
    url(r'^my/stories/draft/$', 'view_my_stories', {'showing_stories': 'draft'}, name='view_my_stories_draft'),
    url(r'^my/stories/published/$', 'view_my_stories', {'showing_stories': 'published'}, name='view_my_stories_published'),

    url(r'^my/story/write/$', 'write_my_story', {'story_uid': ''},
        name='write_my_empty_story'),
    url(r'^my/story/(?P<story_uid>[\w-]+)/write/$', 'write_my_story',
        name='write_my_story'),
    url(r'^my/story/(?P<story_uid>[\w-]+)/publishing/excerpt/$', 'publishing_my_story_excerpt',
        name='publishing_my_story_excerpt'),
    url(r'^my/story/(?P<story_uid>[\w-]+)/publishing/details/$', 'publishing_my_story_details',
        name='publishing_my_story_details'),
    url(r'^my/story/(?P<story_uid>[\w-]+)/publishing/confirm/$', 'publishing_my_story_confirm',
        name='publishing_my_story_confirm'),

    url(r'^my/story/(?P<story_uid>[\w-]+)/edit/$', 'edit_my_story_general', name='edit_my_story_general'),
    url(r'^my/story/(?P<story_uid>[\w-]+)/content/$', 'edit_my_story_content', name='edit_my_story_content'),

    url(r'^ajax/story/(?P<story_uid>[\w-]+)/autosave/$', 'ajax_autosave_editing_story',
        name='ajax_autosave_editing_story'),
    #url(r'^ajax/story/autosave/$', 'ajax_autosave_editing_story', name='ajax_autosave_editing_story'),

    url(r'^ajax/story/image/upload/$', 'ajax_upload_image_editing_story', name='ajax_upload_image_editing_story'),
    url(r'^ajax/story/image/recent/$', 'ajax_recent_image_editing_story', name='ajax_recent_image_editing_story'),
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