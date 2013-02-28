# -*- encoding: utf-8 -*-
from django.contrib import messages
from django.http import Http404

from django.shortcuts import render, redirect
from common.utilities import split_filepath
from presentation.forms import EditProfileForm, EmailChangeForm, NoAutoFillPasswordChangeForm


def view_my_settings_profile(request):
    user = request.user

    if request.method == 'POST':
        form = EditProfileForm(user, request.POST, request.FILES)
        if form.is_valid():
            user.name = form.cleaned_data['name']
            user.url_name = form.cleaned_data['url_name']
            user.bio = form.cleaned_data['bio']
            user.website_url = form.cleaned_data['website_url']
            user.facebook_url = form.cleaned_data['facebook_url']
            user.twitter_url = form.cleaned_data['twitter_url']
            user.save()

            avatar = form.cleaned_data['avatar']
            if avatar:
                if user.avatar:
                    user.avatar.delete()

                (root, name, ext) = split_filepath(avatar.name)
                user.avatar.save('avatar.%s' % ext, avatar)

            messages.success(request, u'บันทึกการเปลี่ยนแปลงเรียบร้อย')
            return redirect('view_my_settings_profile')

    else:
        form = EditProfileForm(user, initial={
            'avatar': user.avatar,
            'name': user.name,
            'url_name': user.url_name,
            'bio': user.bio,
            'website_url': user.website_url,
            'facebook_url': user.facebook_url,
            'twitter_url': user.twitter_url,
        })

    return render(request, 'user/settings/settings_profile.html', {'form': form})


def view_my_settings_account(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'email':
            email_form = EmailChangeForm(request.POST)
            if email_form.is_valid():
                # TODO Send confirmation email again
                request.user.email = email_form.cleaned_data['email']
                request.user.save()

                messages.success(request, u'เปลี่ยนอีเมลเรียบร้อย')
                return redirect('view_my_settings_account')

            else:
                password_form = NoAutoFillPasswordChangeForm(request.user)

        elif request.POST.get('submit') == 'email':
            password_form = NoAutoFillPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                request.user.set_password(password_form.cleaned_data['new_password1'])
                request.user.save()

                messages.success(request, u'เปลี่ยนรหัสผ่านเรียบร้อย')
                return redirect('view_my_settings_account')

            else:
                email_form = EmailChangeForm(initial={'email': request.user.email})
        else:
            raise Http404

    else:
        email_form = EmailChangeForm(initial={'email': request.user.email})
        password_form = NoAutoFillPasswordChangeForm(request.user)

    return render(request, 'user/settings/settings_account.html',
                  {'email_form': email_form, 'password_form': password_form})