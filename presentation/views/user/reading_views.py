# -*- encoding: utf-8 -*-

from django.shortcuts import render


def view_user_library(request):
    return render(request, 'user/settings/settings_profile.html', {})


def read_publication(request):
    return render(request, 'user/settings/settings_account.html', {})