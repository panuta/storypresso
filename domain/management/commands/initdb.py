# -*- encoding: utf-8 -*-

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from domain.models import *


class Command(BaseCommand):
    help = 'Populate initial data to database'

    def handle(self, *args, **options):
        # PRODUCTION CODE ##############################################################################################

        if Site.objects.all().exists():
            Site.objects.all().update(domain=settings.WEBSITE_DOMAIN, name=settings.WEBSITE_NAME)
        else:
            Site.objects.get_or_create(domain=settings.WEBSITE_DOMAIN, name=settings.WEBSITE_NAME)

        some_admin = None
        for admin in settings.ADMINS:
            try:
                user = UserAccount.objects.get(email=admin[1])
            except UserAccount.DoesNotExist:
                user = UserAccount.objects.create_superuser(admin[1], admin[0], '1q2w3e4r')

            some_admin = user

        # DEVELOPMENT CODE #############################################################################################

        if settings.DEBUG:

            # Writers
            try:
                writer1 = UserAccount.objects.get(email='writer1@example.com')
            except UserAccount.DoesNotExist:
                writer1 = UserAccount.objects.create_user('writer1@example.com', 'Writer1', '1q2w3e4r')

            try:
                writer2 = UserAccount.objects.get(email='writer2@example.com')
            except UserAccount.DoesNotExist:
                writer2 = UserAccount.objects.create_user('writer2@example.com', 'Writer2', '1q2w3e4r')

            try:
                writer3 = UserAccount.objects.get(email='writer3@example.com')
            except UserAccount.DoesNotExist:
                writer3 = UserAccount.objects.create_user('writer3@example.com', 'Writer3', '1q2w3e4r')


            # Stories Created

            try:
                story1 = Story.objects.get(title='ความน่าจะเป็นที่นี่จะเป็นชื่อเรื่อง 1', created_by=writer1)
            except Story.DoesNotExist:
                story1 = Story.objects.create(
                    title='ความน่าจะเป็นที่นี่จะเป็นชื่อเรื่อง 1',
                    summary='โต๋เต๋ วอฟเฟิลมอยส์เจอไรเซอร์ฮอตแคมป์ติ๋ม โค้ชซะ ช็อปเจ๊าะแจ๊ะ อพาร์ทเมนต์ชัวร์สติ๊กเกอร์รองรับว้าว อิเหนาคาวบอยหม่านโถวออเดอร์เคลียร์บุ๋น บุญคุณเซ็กส์มาร์กไลน์ แลนด์ราชานุญาตแอปเปิ้ล',
                    excerpt='คอนโดแฮมเบอร์เกอร์สเปกลิมิต ดีไซน์เนอร์โบว์เซี้ยวนอร์ท บลอนด์ออร์เดอร์เวสต์ซิงอีสต์ แจม เพาเวอร์บลูเบอร์รี่เฟอร์รี่โฟน เอ๋อพิซซ่าเซ็กซ์ออดิชั่น มหาอุปราชาโพลารอยด์เบิร์น โรลออนแคมป์สงบสุขเห่ยซิลเวอร์ แต๋วรีทัชเทรลเล่อร์ตรวจทานคอนแท็คเลดี้',
                    price=14.00,
                    is_draft=False,
                    created_by=writer1,
                    published_on=now(),
                )

                story_content1 = StoryContent.objects.create(story=story1, body='คอนโดแฮมเบอร์เกอร์สเปกลิมิต ดีไซน์เนอร์โบว์เซี้ยวนอร์ท บลอนด์ออร์เดอร์เวสต์ซิงอีสต์ แจม เพาเวอร์บลูเบอร์รี่เฟอร์รี่โฟน เอ๋อพิซซ่าเซ็กซ์ออดิชั่น มหาอุปราชาโพลารอยด์เบิร์น โรลออนแคมป์สงบสุขเห่ยซิลเวอร์ แต๋วรีทัชเทรลเล่อร์ตรวจทานคอนแท็คเลดี้')

            try:
                story2 = Story.objects.get(title='ความน่าจะเป็นที่นี่จะเป็นชื่อเรื่อง 2', created_by=writer1)
            except Story.DoesNotExist:
                story2 = Story.objects.create(
                    title='ความน่าจะเป็นที่นี่จะเป็นชื่อเรื่อง 2',
                    summary='โต๋เต๋ วอฟเฟิลมอยส์เจอไรเซอร์ฮอตแคมป์ติ๋ม โค้ชซะ ช็อปเจ๊าะแจ๊ะ อพาร์ทเมนต์ชัวร์สติ๊กเกอร์รองรับว้าว อิเหนาคาวบอยหม่านโถวออเดอร์เคลียร์บุ๋น บุญคุณเซ็กส์มาร์กไลน์ แลนด์ราชานุญาตแอปเปิ้ล',
                    excerpt='คอนโดแฮมเบอร์เกอร์สเปกลิมิต ดีไซน์เนอร์โบว์เซี้ยวนอร์ท บลอนด์ออร์เดอร์เวสต์ซิงอีสต์ แจม เพาเวอร์บลูเบอร์รี่เฟอร์รี่โฟน เอ๋อพิซซ่าเซ็กซ์ออดิชั่น มหาอุปราชาโพลารอยด์เบิร์น โรลออนแคมป์สงบสุขเห่ยซิลเวอร์ แต๋วรีทัชเทรลเล่อร์ตรวจทานคอนแท็คเลดี้',
                    price=24.00,
                    is_draft=True,
                    created_by=writer1,
                )

                story_content2 = StoryContent.objects.create(story=story2, body='คอนโดแฮมเบอร์เกอร์สเปกลิมิต ดีไซน์เนอร์โบว์เซี้ยวนอร์ท บลอนด์ออร์เดอร์เวสต์ซิงอีสต์ แจม เพาเวอร์บลูเบอร์รี่เฟอร์รี่โฟน เอ๋อพิซซ่าเซ็กซ์ออดิชั่น มหาอุปราชาโพลารอยด์เบิร์น โรลออนแคมป์สงบสุขเห่ยซิลเวอร์ แต๋วรีทัชเทรลเล่อร์ตรวจทานคอนแท็คเลดี้')

            try:
                story3 = Story.objects.get(title='ความน่าจะเป็นที่นี่จะเป็นชื่อเรื่อง 3', created_by=writer1)
            except Story.DoesNotExist:
                story3 = Story.objects.create(
                    title='ความน่าจะเป็นที่นี่จะเป็นชื่อเรื่อง 3',
                    summary='โต๋เต๋ วอฟเฟิลมอยส์เจอไรเซอร์ฮอตแคมป์ติ๋ม โค้ชซะ ช็อปเจ๊าะแจ๊ะ อพาร์ทเมนต์ชัวร์สติ๊กเกอร์รองรับว้าว อิเหนาคาวบอยหม่านโถวออเดอร์เคลียร์บุ๋น บุญคุณเซ็กส์มาร์กไลน์ แลนด์ราชานุญาตแอปเปิ้ล',
                    excerpt='คอนโดแฮมเบอร์เกอร์สเปกลิมิต ดีไซน์เนอร์โบว์เซี้ยวนอร์ท บลอนด์ออร์เดอร์เวสต์ซิงอีสต์ แจม เพาเวอร์บลูเบอร์รี่เฟอร์รี่โฟน เอ๋อพิซซ่าเซ็กซ์ออดิชั่น มหาอุปราชาโพลารอยด์เบิร์น โรลออนแคมป์สงบสุขเห่ยซิลเวอร์ แต๋วรีทัชเทรลเล่อร์ตรวจทานคอนแท็คเลดี้',
                    price=34.00,
                    is_draft=True,
                    created_by=writer1,
                )

                story_content3 = StoryContent.objects.create(story=story3, body='คอนโดแฮมเบอร์เกอร์สเปกลิมิต ดีไซน์เนอร์โบว์เซี้ยวนอร์ท บลอนด์ออร์เดอร์เวสต์ซิงอีสต์ แจม เพาเวอร์บลูเบอร์รี่เฟอร์รี่โฟน เอ๋อพิซซ่าเซ็กซ์ออดิชั่น มหาอุปราชาโพลารอยด์เบิร์น โรลออนแคมป์สงบสุขเห่ยซิลเวอร์ แต๋วรีทัชเทรลเล่อร์ตรวจทานคอนแท็คเลดี้')

            # Readers
            try:
                reader1 = UserAccount.objects.get(email='reader1@example.com')
            except UserAccount.DoesNotExist:
                reader1 = UserAccount.objects.create_user('reader1@example.com', 'Reader1', '1q2w3e4r')

            try:
                reader2 = UserAccount.objects.get(email='reader2@example.com')
            except UserAccount.DoesNotExist:
                reader2 = UserAccount.objects.create_user('reader2@example.com', 'Reader2', '1q2w3e4r')

            try:
                reader3 = UserAccount.objects.get(email='reader3@example.com')
            except UserAccount.DoesNotExist:
                reader3 = UserAccount.objects.create_user('reader3@example.com', 'Reader3', '1q2w3e4r')

            # Stories Purchased
            # TODO

