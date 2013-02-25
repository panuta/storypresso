# -*- encoding: utf-8 -*-

from django.shortcuts import render


def view_user_works(request):
    return render(request, 'user/room_works.html', {})


def write_user_work(request):
    return render(request, 'user/room_works_writing.html', {})