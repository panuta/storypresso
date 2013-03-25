# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from domain.models import StoryPurchase


@login_required
def view_my_shelves(request):
    purchases = StoryPurchase.objects.filter(user=request.user)
    return render(request, 'user/shelves.html', {'purchases': purchases})

