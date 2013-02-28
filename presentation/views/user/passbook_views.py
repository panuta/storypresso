# -*- encoding: utf-8 -*-

from django.shortcuts import render


def view_my_passbook(request):
    return render(request, 'user/passbook.html', {})
