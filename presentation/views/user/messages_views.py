# -*- encoding: utf-8 -*-

from django.shortcuts import render


def view_my_messages(request):
    return render(request, 'user/messages.html', {})
