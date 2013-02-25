# -*- encoding: utf-8 -*-

from django.shortcuts import render


def view_user_safebox(request):
    return render(request, 'user/room_safebox.html', {})
