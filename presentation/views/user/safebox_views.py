# -*- encoding: utf-8 -*-

from django.shortcuts import render


def view_my_safebox(request):
    return render(request, 'user/safebox.html', {})
