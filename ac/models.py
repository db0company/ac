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
    name = models.CharField(_('Island name'), max_length=100)
    character_name = models.CharField(_('Character name'), max_length=100)

    NATIVE_FRUIT_CHOICES = [
        'Pear',
        'Coconut',
        'Apple',
        'Peach',
        'Cherry',
        'Orange',
    ]
    i_native_fruit = models.PositiveIntegerField('Native fruit', choices=i_choices(NATIVE_FRUIT_CHOICES), null=True)

    title = models.CharField(_('Title'), null=True, max_length=100)
    message = models.TextField(_('Message'), null=True, max_length=512)

    friend_id = models.CharField('Nintendo Friend code', null=True, max_length=100)
    show_friend_id = models.BooleanField(_('Should your friend code be visible to other players?'), default=True)

    photo = models.ForeignKey('magi.Activity', null=True, limit_choices_to=Q(
        Q(c_tags__contains="photo")
        & Q(image__isnull=False)
        & ~Q(image='')
    ), help_text=mark_safe('<a class="btn btn-main btn-sm" target="_blank" href="/activities/add/">Add photo</a> (make sure you tag "Photo")'))

    _thumbnail_screenshot = models.ImageField(null=True, upload_to=uploadThumb('account_screenshot'))
    screenshot = models.ImageField(
        'Passport', help_text='Screenshot of in-game passport',
        upload_to=uploadItem('account_screenshot'), null=True)

    @property
    def center(self):
        return AttrDict({
            'art': self.photo.image,
            'art_url': self.photo.image_url,
            'art_url_original': self.photo.image_url,
            'color': None,
        })

    display_nickname = property(lambda _s: _s.name)

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
    villager = models.ForeignKey(Villager, related_name='accounts')

    @property
    def image(self):
        return self.villager.image

    def __unicode__(self):
        return unicode(self.villager)
