# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from common.constants.categories import CATEGORY_CHOICES_WITH_BLANK

from domain.models import UserAccount


# STORY ################################################################################################################

class WriteStoryForm(forms.Form):
    uid = forms.CharField(max_length=40, widget=forms.HiddenInput)
    title = forms.CharField(required=False, max_length=500, widget=forms.TextInput(attrs={'placeholder': 'ตั้งชื่อเรื่อง'}))
    body = forms.CharField(required=False, widget=forms.Textarea)


class PublishStoryForm(forms.Form):
    excerpt = forms.CharField(required=False, max_length=5000)
    cover_small = forms.ImageField(required=False, widget=forms.FileInput())
    cover_full = forms.ImageField(required=False, widget=forms.FileInput())
    category = forms.ChoiceField(required=False, choices=CATEGORY_CHOICES_WITH_BLANK)
    title = forms.CharField(required=False, max_length=500)
    summary = forms.CharField(required=False, max_length=1000)
    price = forms.DecimalField(required=False, max_digits=10, decimal_places=2, min_value=9.00)


# USER SETTINGS ########################################################################################################

class EditProfileForm(forms.Form):
    avatar = forms.ImageField(required=False, widget=forms.FileInput())
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'span5'}))
    url_name = forms.SlugField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'span3'}))
    bio = forms.CharField(required=False, max_length=300, widget=forms.Textarea(attrs={'class': 'span7'}))
    website_url = forms.URLField(required=False, max_length=200, widget=forms.TextInput(attrs={'class': 'span5'}))
    facebook_url = forms.URLField(required=False, max_length=200, widget=forms.TextInput(attrs={'class': 'span5'}))
    twitter_url = forms.URLField(required=False, max_length=200, widget=forms.TextInput(attrs={'class': 'span5'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        forms.Form.__init__(self, *args, **kwargs)

    def clean_url_name(self):
        url_name = self.cleaned_data.get('url_name').lower()

        if UserAccount.objects.filter(url_name=url_name).exclude(url_name='').exclude(id=self.user.id).exists():
            raise forms.ValidationError(_('URL name นี้มีคนใช้แล้ว'))

        return url_name


class EmailChangeForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'span4'}))


class NoAutoFillPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'span4'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'span4'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'span4'}))