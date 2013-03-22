# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from domain.models import UserAccount


def view_user_profile_by_id(request, user_uid):
    user = get_object_or_404(UserAccount, user_uid=user_uid)
    return _view_user_profile(request, user)


def view_user_profile_by_url_name(request, url_name):
    user = get_object_or_404(UserAccount, url_name=url_name)
    return _view_user_profile(request, user)


def _view_user_profile(request, user):
    #publications = Publication.objects.filter(created_by=user)
    #return render(request, 'accounts/user_profile.html', {'profile_user':user, 'publications':publications})
    return render(request, 'user/profile.html', {'profile_user': user, })


def view_my_shelves(request):
    return render(request, 'user/shelves.html', {})