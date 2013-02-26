# -*- encoding: utf-8 -*-

from django.shortcuts import render

def view_homepage(request):
    print request.user.is_authenticated()
    return render(request, 'homepage.html', {})