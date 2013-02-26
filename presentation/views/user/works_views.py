# -*- encoding: utf-8 -*-

from django.shortcuts import render


def view_user_works(request):
    return render(request, 'user/workroom.html', {})


def write_user_work(request):
    return render(request, 'user/workroom_writing.html', {})