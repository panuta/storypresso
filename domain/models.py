# -*- encoding: utf-8 -*-

import random
import uuid

from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.crypto import salted_hmac
from django.utils.translation import ugettext_lazy as _

import shortuuid
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer
from common.email import send_bot_email
from presentation.exceptions import PublishingException

SHORTUUID_ALPHABETS_FOR_ID = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


# ACCOUNT ##############################################################################################################

class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError(_('Users must have an email address'))

        if not name:
            raise ValueError(_('Users must have a name'))

        user = UserAccount.objects.create(
            email=UserAccountManager.normalize_email(email),
            name=name,
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
    return 'users/%s/%s' % (instance.uid, filename)


class UserAccount(AbstractBaseUser):
    uid = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    url_name = models.CharField(max_length=100, db_index=True, blank=True, default='')

    name = models.CharField(max_length=300)
    bio = models.CharField(max_length=2000)
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
        if not self.uid:
            uuid = None

            while not uuid:
                shortuuid.set_alphabet(SHORTUUID_ALPHABETS_FOR_ID)
                uuid = shortuuid.uuid()[:10]

                try:
                    UserAccount.objects.get(uid=uuid)
                except UserAccount.DoesNotExist:
                    pass
                else:
                    uuid = None

            self.uid = uuid

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
        return reverse('view_user_profile_by_id', args=[self.uid])

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


class UserRegistrationManager(models.Manager):
    def create_registration(self, email):
        key_salt = 'accounts.models.UserRegistrationManager_%d' % random.randint(1, 99999999)
        email = email.encode('utf-8')
        value = email
        registration_key = salted_hmac(key_salt, value).hexdigest()

        return self.create(email=email, registration_key=registration_key)


class UserRegistration(models.Model):
    email = models.CharField(max_length=254)
    registration_key = models.CharField(max_length=200, unique=True, db_index=True)
    registered = models.DateTimeField(auto_now_add=True)

    objects = UserRegistrationManager()

    def send_registration_request(self):
        email_context = {'settings': settings, 'registration': self}

        subject = _('StoryPresso Registration Confirmation')
        text_email_body = render_to_string('accounts/emails/registration_email.txt', email_context)
        html_email_body = render_to_string('accounts/emails/registration_email.html', email_context)

        send_bot_email([self.email], subject, text_email_body, html_email_body)

        return True

    def claim_registration(self, name, password):
        user_account = UserAccount.objects.create_user(self.email, name, password)
        return user_account

    def __unicode__(self):
        return '%s has key %s' % (self.email, self.registration_key)


# PUBLICATION ##########################################################################################################

def story_cover_dir(instance, filename):
    return 'users/%s/stories/%s' % (instance.created_by.uid, filename)


class StoryManager(models.Manager):
    def generate_uuid(self):
        uid = None

        while not uid:
            uid = str(uuid.uuid4())

            try:
                self.get(uid=uid)
            except Story.DoesNotExist:
                pass
            else:
                uid = None

        return uid


class Story(models.Model):
    uid = models.CharField(max_length=50)
    title = models.CharField(max_length=500, blank=True, default='')
    summary = models.TextField(blank=True, default='')
    cover_small = ThumbnailerImageField(upload_to=story_cover_dir, blank=True, null=True)
    cover_large = ThumbnailerImageField(upload_to=story_cover_dir, blank=True, null=True)
    excerpt = models.TextField(blank=True, default='')
    primary_category = models.CharField(max_length=50, blank=True, default='')
    secondary_category = models.CharField(max_length=50, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    is_draft = models.BooleanField(default=True)
    created_by = models.ForeignKey('UserAccount', related_name='stories_created')
    created_on = models.DateTimeField(default=timezone.now())
    modified_on = models.DateTimeField(default=timezone.now())
    published_on = models.DateTimeField(null=True)

    objects = StoryManager()

    class Meta:
        ordering = ['-published_on']

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = Story.objects.generate_uuid()

        models.Model.save(self, *args, **kwargs)

    def large_cover_url(self):
        if self.cover_large:
            return get_thumbnailer(self.avatar)['cover_large'].url
        return '%simages/%s' % (settings.STATIC_URL, settings.STORY_COVER_DEFAULT_LARGE)

    def small_cover_url(self):
        if self.cover_small:
            return get_thumbnailer(self.avatar)['cover_small'].url
        return '%simages/%s' % (settings.STATIC_URL, settings.STORY_COVER_DEFAULT_SMALL)

    def tiny_cover_url(self):
        if self.cover_small:
            return get_thumbnailer(self.avatar)['cover_tiny'].url
        return '%simages/%s' % (settings.STATIC_URL, settings.STORY_COVER_DEFAULT_TINY)

    def is_ready_to_publish(self):
        # TODO Check empty, empty HTML tag
        # TODO Check content

        if not self.title or not self.content.body:
            raise PublishingException(u'ชื่อเรื่องหรือเนื้อหายังว่างอยู่ กรุณาใส่ให้ครบถ้วนก่อนตีพิมพ์')

        return


class StoryContent(models.Model):
    story = models.OneToOneField('Story', related_name='content')
    body = models.TextField(blank=True, default='')


class EditingStory(models.Model):
    story = models.OneToOneField('Story', related_name='editing')
    title = models.CharField(max_length=500, blank=True, default='')
    created_on = models.DateTimeField(default=timezone.now())


class StoryEditingContent(models.Model):
    editing_story = models.OneToOneField('EditingStory', related_name='editing_content')
    body = models.TextField(blank=True, default='')


# STORY PURCHASE #######################################################################################################

class StoryPurchase(models.Model):
    uid = models.CharField(max_length=50)
    story = models.ForeignKey('Story', related_name='purchases')
    user = models.ForeignKey('UserAccount', related_name='purchases')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_on = models.DateTimeField(default=timezone.now())



