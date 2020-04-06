# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('ac', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='_thumbnail_character_photo',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadThumb(b'account_character_photo')),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='_thumbnail_island_map',
            field=models.ImageField(null=True, upload_to=magi.utils.uploadThumb(b'account_island_map')),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='accept_friend_requests',
            field=models.NullBooleanField(verbose_name='Accept friend requests'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='best_friend',
            field=models.ForeignKey(related_name='best_friends', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Best friend', to='ac.AddedVillager', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='character_photo',
            field=models.ImageField(upload_to=magi.utils.uploadItem(b'account_character_photo'), null=True, verbose_name=b'Character photo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='island_map',
            field=models.ImageField(help_text=b'Screenshot of island map <img src="https://i.imgur.com/SmL86yK.jpg" height="40" class="pull-right">', upload_to=magi.utils.uploadItem(b'account_island_map'), null=True, verbose_name=b'Island Map'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='message',
            field=models.TextField(max_length=512, null=True, verbose_name='Passport message'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='photo',
            field=models.ForeignKey(verbose_name=b'Cover photo', to='magi.Activity', help_text=b'<a class="btn btn-main btn-sm" target="_blank" href="/activities/add/">Add photo</a> (make sure you tag "Photo")', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='screenshot',
            field=models.ImageField(help_text=b'Screenshot of in-game passport <img src="https://i.imgur.com/s7Wgzoc.png" height="40" class="pull-right">', upload_to=magi.utils.uploadItem(b'account_screenshot'), null=True, verbose_name=b'Passport'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='title',
            field=models.CharField(max_length=100, null=True, verbose_name='Passport title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='addedvillager',
            name='villager',
            field=models.ForeignKey(related_name='accounts', verbose_name='Villager', to='ac.Villager'),
            preserve_default=True,
        ),
    ]
