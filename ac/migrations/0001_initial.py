# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('magi', '0051_auto_20200405_1026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_cache_owner_last_update', models.DateTimeField(null=True)),
                ('_cache_owner_username', models.CharField(max_length=32, null=True)),
                ('_cache_owner_email', models.EmailField(max_length=75, blank=True)),
                ('_cache_owner_preferences_i_status', models.CharField(max_length=12, null=True)),
                ('_cache_owner_preferences_twitter', models.CharField(max_length=32, null=True, blank=True)),
                ('_cache_owner_color', models.CharField(max_length=100, null=True, blank=True)),
                ('creation', models.DateTimeField(auto_now_add=True, verbose_name='Join date')),
                ('nickname', models.CharField(help_text="Give a nickname to your account to easily differentiate it from your other accounts when you're managing them.", max_length=200, null=True, verbose_name='Nickname')),
                ('start_date', models.DateField(null=True, verbose_name='Start date', validators=[magi.utils.PastOnlyValidator])),
                ('level', models.PositiveIntegerField(null=True, verbose_name='Level')),
                ('default_tab', models.CharField(max_length=100, null=True, verbose_name='Default tab')),
                ('_cache_leaderboards_last_update', models.DateTimeField(null=True)),
                ('_cache_leaderboard', models.PositiveIntegerField(null=True)),
                ('name', models.CharField(max_length=100, verbose_name='Island name')),
                ('character_name', models.CharField(max_length=100, verbose_name='Character name')),
                ('i_native_fruit', models.PositiveIntegerField(null=True, verbose_name=b'Native fruit', choices=[(0, b'Pear'), (1, b'Coconut'), (2, b'Apple'), (3, b'Peach'), (4, b'Cherry'), (5, b'Orange')])),
                ('title', models.CharField(max_length=100, null=True, verbose_name='Title')),
                ('message', models.TextField(max_length=512, null=True, verbose_name='Message')),
                ('friend_id', models.CharField(max_length=100, null=True, verbose_name=b'Nintendo Friend code')),
                ('show_friend_id', models.BooleanField(default=True, verbose_name='Should your friend code be visible to other players?')),
                ('_thumbnail_screenshot', models.ImageField(null=True, upload_to=magi.utils.uploadThumb(b'account_screenshot'))),
                ('screenshot', models.ImageField(help_text=b'Screenshot of in-game passport', upload_to=magi.utils.uploadItem(b'account_screenshot'), null=True, verbose_name=b'Passport')),
                ('owner', models.ForeignKey(related_name='accounts', to=settings.AUTH_USER_MODEL)),
                ('photo', models.ForeignKey(to='magi.Activity', help_text=b'<a class="btn btn-main btn-sm" target="_blank" href="/activities/add/">Add photo</a> (make sure you tag "Photo")', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AddedVillager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_cache_account_last_update', models.DateTimeField(null=True)),
                ('_cache_j_account', models.TextField(null=True)),
                ('account', models.ForeignKey(related_name='added_villagers', to='ac.Account')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Villager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'villager'), null=True, verbose_name='Image')),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name', db_index=True)),
                ('species', models.CharField(max_length=100, null=True, verbose_name='Species')),
                ('i_gender', models.PositiveIntegerField(default=2, verbose_name='Gender', choices=[(0, b'Male'), (1, b'Female'), (2, b'Other')])),
                ('personality', models.CharField(max_length=100, null=True, verbose_name='Personality')),
                ('owner', models.ForeignKey(related_name='added_villagers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='addedvillager',
            name='villager',
            field=models.ForeignKey(related_name='accounts', to='ac.Villager'),
            preserve_default=True,
        ),
    ]
