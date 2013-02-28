# -*- encoding: utf-8 -*-

from django.shortcuts import render


def view_my_works(request):
    return render(request, 'user/workroom.html', {})


def write_my_work(request):
    return render(request, 'user/workroom_writing.html', {})


def publish_my_work(request):
    return render(request, 'user/workroom_publishing.html', {})