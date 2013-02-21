# -*- encoding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

import shortuuid
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer

SHORTUUID_ALPHABETS_FOR_ID = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


# ACCOUNTS #############################################################################################################

class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError(_('Users must have an email address'))

        if not name:
            raise ValueError(_('Users must have a name'))

        user = UserAccount.objects.create(
            email = UserAccountManager.normalize_email(email),
            name = name,
            )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_admin = True
        user.save()
        return user


def user_image_dir(instance, filename):
    return 'users/%s/%s' % (instance.user_uid, filename)


class UserAccount(AbstractBaseUser):
    user_uid = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    url_name = models.CharField(max_length=100, db_index=True, blank=True, default='')

    name = models.CharField(max_length=300)
    bio = models.CharField(max_length=1000)
    avatar = ThumbnailerImageField(upload_to=user_image_dir, blank=True, null=True)

    website_url = models.CharField(max_length=200, blank=True, default='')
    facebook_url = models.CharField(max_length=200, blank=True, default='')
    twitter_url = models.CharField(max_length=200, blank=True, default='')

    date_joined = models.DateTimeField(default=timezone.now())
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def save(self, *args, **kwargs):
        if not self.user_uid:
            uuid = None

            while not uuid:
                shortuuid.set_alphabet(SHORTUUID_ALPHABETS_FOR_ID)
                uuid = shortuuid.uuid()[:10]

                try:
                    UserAccount.objects.get(user_uid=uuid)
                except UserAccount.DoesNotExist:
                    pass
                else:
                    uuid = None

            self.user_uid = uuid

        models.Model.save(self, *args, **kwargs)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        if ' ' in self.name:
            return self.name.split(' ')[0]
        return self.name

    def __unicode__(self):
        return '%s <%s>' % (self.name, self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.is_admin

    # URL

    def get_profile_url(self):
        if self.url_name:
            return reverse('view_user_profile_by_url_name', args=[self.url_name])
        return reverse('view_user_profile_by_id', args=[self.user_uid])

    # Avatars

    def get_normal_avatar_url(self):
        if self.avatar:
            return get_thumbnailer(self.avatar)['avatar_normal'].url
        return '%simages/%s' % (settings.STATIC_URL, settings.USER_AVATAR_DEFAULT_NORMAL)

    def get_small_avatar_url(self):
        if self.avatar:
            return get_thumbnailer(self.avatar)['avatar_small'].url
        return '%simages/%s' % (settings.STATIC_URL, settings.USER_AVATAR_DEFAULT_SMALL)

    def get_smaller_avatar_url(self):
        if self.avatar:
            return get_thumbnailer(self.avatar)['avatar_smaller'].url
        return '%simages/%s' % (settings.STATIC_URL, settings.USER_AVATAR_DEFAULT_SMALLER)

    def get_tiny_avatar_url(self):
        if self.avatar:
            return get_thumbnailer(self.avatar)['avatar_tiny'].url
        return '%simages/%s' % (settings.STATIC_URL, settings.USER_AVATAR_DEFAULT_TINY)

