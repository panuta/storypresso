# -*- encoding: utf-8 -*-

from django.shortcuts import render


def view_my_transaction(request):
    return render(request, 'user/transaction.html', {})
