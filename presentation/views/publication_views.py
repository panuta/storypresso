# -*- encoding: utf-8 -*-

from django.shortcuts import render


def view_publication(request):
    return render(request, 'publication/publication_view.html', {})


def read_publication(request):
    return render(request, 'publication/publication_read.html', {})