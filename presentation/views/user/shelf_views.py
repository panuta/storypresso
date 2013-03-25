# -*- encoding: utf-8 -*-

from django.shortcuts import render


def view_my_shelves(request):
    return render(request, 'user/shelves.html', {})