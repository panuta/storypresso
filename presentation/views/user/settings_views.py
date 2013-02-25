# -*- encoding: utf-8 -*-

from django.shortcuts import render


def view_user_settings_profile(request):
    return render(request, 'user/room_settings_profile.html', {})


def view_user_settings_account(request):
    return render(request, 'user/room_settings_account.html', {})