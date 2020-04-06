from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.db import models
from django.utils.safestring import mark_safe
from magi.abstract_models import BaseAccount
from magi.item_model import (
    MagiModel,
    i_choices,
)
from magi.abstract_models import (
    AccountAsOwnerModel,
)
from magi.utils import (
    AttrDict,
    uploadThumb,
    uploadItem,
)

############################################################
# Account (= island)

class Account(BaseAccount):
    character_name = models.CharField(_('Character name'), max_length=100)

    character_photo = models.ImageField('Character photo', upload_to=uploadItem('account_character_photo'), null=True)
    _thumbnail_character_photo = models.ImageField(null=True, upload_to=uploadThumb('account_character_photo'))

    name = models.CharField(_('Island name'), max_length=100)

    title = models.CharField(_('Passport title'), null=True, max_length=100)
    message = models.TextField(_('Passport message'), null=True, max_length=512)

    NATIVE_FRUIT_CHOICES = [
        'Pear',
        'Coconut',
        'Apple',
        'Peach',
        'Cherry',
        'Orange',
    ]
    i_native_fruit = models.PositiveIntegerField('Native fruit', choices=i_choices(NATIVE_FRUIT_CHOICES), null=True)

    best_friend = models.ForeignKey('AddedVillager', on_delete=models.SET_NULL, null=True, verbose_name='Best friend', related_name='best_friends')

    friend_id = models.CharField('Nintendo Friend code', null=True, max_length=100)
    show_friend_id = models.BooleanField(_('Should your friend code be visible to other players?'), default=True)
    accept_friend_requests = models.NullBooleanField(_('Accept friend requests'), null=True)

    screenshot = models.ImageField(
        'Passport', help_text=mark_safe(
            'Screenshot of in-game passport <img src="https://i.imgur.com/s7Wgzoc.png" height="40" class="pull-right">'
        ), upload_to=uploadItem('account_screenshot'), null=True)
    _thumbnail_screenshot = models.ImageField(null=True, upload_to=uploadThumb('account_screenshot'))

    island_map = models.ImageField(
        'Island Map', upload_to=uploadItem('account_island_map'), null=True, help_text=mark_safe(
            'Screenshot of island map <img src="https://i.imgur.com/SmL86yK.jpg" height="40" class="pull-right">'
        ))
    _thumbnail_island_map = models.ImageField(null=True, upload_to=uploadThumb('account_island_map'))

    photo = models.ForeignKey('magi.Activity', null=True, limit_choices_to=Q(
        Q(c_tags__contains="photo")
        & Q(image__isnull=False)
        & ~Q(image='')
    ), help_text=mark_safe('<a class="btn btn-main btn-sm" target="_blank" href="/activities/add/">Add photo</a> (make sure you tag "Photo")'), verbose_name='Cover photo')

    @property
    def center(self):
        return AttrDict({
            'art': self.photo.image,
            'art_url': self.photo.image_url,
            'art_url_original': self.photo.image_url,
            'color': None,
        })

    display_nickname = property(lambda _s: _s.name)
    display_level = property(lambda _s: _s.character_name)

    def __unicode__(self):
        return u'{} by {}'.format(self.name, self.character_name)

############################################################
# Villager

class Villager(MagiModel):
    collection_name = 'villager'

    owner = models.ForeignKey(User, related_name='added_villagers')

    image = models.ImageField(_('Image'), upload_to=uploadItem('villager'), null=True)

    name = models.CharField(_('Name'), max_length=100, unique=True, db_index=True)

    species = models.CharField(_('Species'), max_length=100, null=True)

    GENDER_CHOICES = (
        'Male',
        'Female',
        'Other',
    )
    i_gender = models.PositiveIntegerField(_('Gender'), choices=i_choices(GENDER_CHOICES), default=2)

    personality = models.CharField(_('Personality'), max_length=100, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

############################################################
# Added villager

class AddedVillager(AccountAsOwnerModel):
    collection_name = 'addedvillager'

    account = models.ForeignKey(Account, related_name='added_villagers', db_index=True)
    villager = models.ForeignKey(Villager, related_name='accounts', verbose_name=_('Villager'))

    @property
    def image(self):
        return self.villager.image

    def __unicode__(self):
        return unicode(self.villager)
