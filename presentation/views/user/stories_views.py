# -*- encoding: utf-8 -*-
import urllib2

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from common.shortcuts import response_json_success
from common.utilities import clean_content

from domain.models import Story, StoryEditingContent, EditingStory, StoryContent
from presentation.exceptions import PublishingException
from presentation.forms import WriteStoryForm, PublishStoryForm


@login_required
def view_my_stories(request, showing_stories):

    if showing_stories == 'all':
        stories = Story.objects.filter(created_by=request.user)

    elif showing_stories == 'draft':
        stories = Story.objects.filter(created_by=request.user, is_draft=True)

    elif showing_stories == 'published':
        stories = Story.objects.filter(created_by=request.user, is_draft=False)

    else:
        raise Http404

    return render(request, 'user/stories.html', {'stories': stories, 'showing_stories': showing_stories})


@login_required
def write_my_story(request, story_uid):
    if not story_uid:
        story = None
        story_content = None
    else:
        story = get_object_or_404(Story, uid=story_uid)
        if story.created_by.id != request.user.id:
            raise Http404
        story_content, created = StoryContent.objects.get_or_create(story=story)

    if request.method == 'POST':
        form = WriteStoryForm(request.POST)
        if form.is_valid():
            uid = form.cleaned_data['uid']

            if story and story.uid != uid:
                raise Http404

            if not story:
                try:
                    story = Story.objects.get(uid=uid)  # Maybe this story is already saved via autosave
                    story_content = story.content
                except Story.DoesNotExist:
                    story = Story.objects.create(uid=uid, created_by=request.user)
                    story_content = StoryContent.objects.create(story=story)

            story.title = form.cleaned_data['title'].strip()
            story.save()

            story_content.body = clean_content(form.cleaned_data['body'])
            story_content.save()

            try:
                editing_story = EditingStory.objects.get(story=story).delete()
                StoryEditingContent.objects.filter(editing_story=editing_story).delete()
            except EditingStory.DoesNotExist:
                pass

            submit_method = request.POST.get('submit')
            if submit_method == 'publish':
                try:
                    story.is_ready_to_publish()
                except PublishingException, e:
                    messages.error(request, e.message)
                    return redirect('write_my_story', story.uid)

                return redirect('publishing_my_story_excerpt', story.uid)

            else:
                messages.success(request, u'บันทึกข้อมูลเรียบร้อย')
                return redirect('write_my_story', story.uid)

        if not story:
            story = Story(uid=request.POST.get('uid'), created_by=request.user)

    else:
        if not story:
            # Pre-generate uuid for Story using when autosave
            story = Story(uid=Story.objects.generate_uuid(), created_by=request.user)
            story_content = StoryContent(story=story)

        form = WriteStoryForm(initial={
            'uid': story.uid,
            'title': story.title,
            'body': story_content.body,
        })

    return render(request, 'user/story_write.html', {'story': story, 'form': form})


@login_required
def publishing_my_story_excerpt(request, story_uid):
    story = get_object_or_404(Story, uid=story_uid)

    if story.created_by.id != request.user.id:
        raise Http404

    if request.method == 'POST':
        form = PublishStoryForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = PublishStoryForm(initial={
            'excerpt': story.excerpt,
            'category': story.primary_category,
            'title': story.title,
            'summary': story.summary,
            'price': story.price,
        })

    return render(request, 'user/story_publish/story_publish_excerpt.html', {'story': story, 'form': form})


@login_required
def publishing_my_story_details(request, story_uid):
    story = get_object_or_404(Story, uid=story_uid)

    if story.created_by.id != request.user.id:
        raise Http404

    return render(request, 'user/story_publish/story_publish_details.html', {'story': story})


@login_required
def publishing_my_story_confirm(request, story_uid):
    story = get_object_or_404(Story, uid=story_uid)

    if story.created_by.id != request.user.id:
        raise Http404

    return render(request, 'user/story_publish/story_publish_confirm.html', {'story': story})


@login_required
def edit_my_story_general(request, story_uid):
    story = get_object_or_404(Story, uid=story_uid)

    if story.created_by.id != request.user.id:
        raise Http404

    if request.method == 'POST':
        pass
    else:
        pass

    return render(request, 'user/story_edit_general.html', {'story': story})


@login_required
def edit_my_story_content(request, story_uid):
    story = get_object_or_404(Story, uid=story_uid)

    if story.created_by.id != request.user.id:
        raise Http404

    if request.method == 'POST':
        form = WriteStoryForm(request.POST)
        if form.is_valid():
            story.title = form.cleaned_data['title']
            story.save()

            story.content.body = clean_content(form.cleaned_data['body'])
            story.content.save()

            submit_method = request.POST.get('submit')
            if submit_method == 'publish':
                if not story.is_draft:
                    messages.warning(request, u'ผลงานนี้ถูกเผยแพร่ไปก่อนหน้านี้แล้ว')
                    return redirect('publish_my_story', story.uid)

                try:
                    story.is_ready_to_publish()
                except PublishingException, e:
                    messages.error(request, e.message)
                    return redirect('edit_my_story_content', story.uid)

                return redirect('publish_my_story', story.uid)

            else:  # DRAFT, SAVE
                messages.success(request, u'บันทึกข้อมูลเรียบร้อย')
                return redirect('edit_my_story_content', story.uid)

    else:
        form = WriteStoryForm(initial={
            'uid': story.uid,
            'title': story.title,
            'body': story.content.body,
        })

    return render(request, 'user/story_edit_content.html', {'story': story, 'form': form})


@csrf_exempt
@require_POST
@login_required
def ajax_autosave_editing_story(request, story_uid):
    try:
        story = Story.objects.get(uid=story_uid)
        if story.created_by.id != request.user.id:
            raise Http404
    except Story.DoesNotExist:
        story = Story.objects.create(uid=story_uid, is_draft=True, created_by=request.user)

    editing_story, created = EditingStory.objects.get_or_create(story=story)
    story_editing_content, created = StoryEditingContent.objects.get_or_create(editing_story=editing_story)

    content = request.POST.get('id_body')
    if content:
        content = urllib2.unquote(content).decode("utf8")
        story_editing_content.body = content
        story_editing_content.save()

    return response_json_success()


def ajax_upload_image_editing_story(request):
    pass


def ajax_recent_image_editing_story(request):
    pass