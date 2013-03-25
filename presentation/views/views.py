# -*- encoding: utf-8 -*-

from django.shortcuts import render
from domain.models import Story


def view_homepage(request):
    recent_stories = Story.objects.filter(is_draft=False).order_by('-published_on')[:9]
    return render(request, 'homepage.html', {'recent_stories': recent_stories})