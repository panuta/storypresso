# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext_lazy as _

from domain.models import UserAccount

class EditProfileForm(forms.Form):
    avatar = forms.ImageField(required=False, widget=forms.FileInput())
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'span5'}))
    url_name = forms.SlugField(required=False, max_length=50, widget=forms.TextInput(attrs={'class':'span3'}))
    bio = forms.CharField(required=False, max_length=300, widget=forms.Textarea(attrs={'class':'span7'}))
    website_url = forms.URLField(required=False, max_length=200, widget=forms.TextInput(attrs={'class':'span5'}))
    facebook_url = forms.URLField(required=False, max_length=200, widget=forms.TextInput(attrs={'class':'span5'}))
    twitter_url = forms.URLField(required=False, max_length=200, widget=forms.TextInput(attrs={'class':'span5'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        forms.Form.__init__(self, *args, **kwargs)

    def clean_url_name(self):
        url_name = self.cleaned_data.get('url_name').lower()

        if UserAccount.objects.filter(url_name=url_name).exclude(url_name='').exclude(id=self.user.id).exists():
            raise forms.ValidationError(_('URL name นี้มีคนใช้แล้ว'))

        return url_name


class EmailChangeForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'span4'}))


class NoAutoFillPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'off', 'class':'span4'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'off', 'class':'span4'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'off', 'class':'span4'}))