# -*- encoding: utf-8 -*-

from django.shortcuts import render


def view_user_messages(request):
    return render(request, 'user/messages.html', {})
