# -*- encoding: utf-8 -*-

from django.shortcuts import render


def view_story(request):
    return render(request, 'story/story_view.html', {})


def read_story(request):
    return render(request, 'story/story_read.html', {})