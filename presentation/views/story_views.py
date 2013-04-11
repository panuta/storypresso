# -*- encoding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from domain.models import Story


def view_story(request, story_uid):
    story = get_object_or_404(Story, uid=story_uid)
    return render(request, 'story/story_view.html', {'story': story})


def read_story(request, story_uid):
    story = get_object_or_404(Story, uid=story_uid)
    return render(request, 'story/story_read.html', {'story': story})