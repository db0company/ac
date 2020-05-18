import operator
from collections import OrderedDict
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.db import models
from django.utils.formats import date_format
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
# Account (= character)

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
# Item
# # todo
#         ('virtual', [
#             'Achievements',
#             'Reactions',
#         ]),

class Item(MagiModel):
    collection_name = 'item'

    owner = models.ForeignKey(User, related_name='added_items')

    name = models.CharField(_('Name'), max_length=100, db_index=True)

    CATEGORIES = OrderedDict([
        (('furnitures', _('Furnitures')), [
            ('Housewares', _('Housewares')),
            ('Miscellaneous', _('Miscellaneous')),
            ('Wall-mounted', _('Wall-mounted')),
            ('Wallpaper', _('Wallpapers')),
            ('Floors', _('Floors')),
            ('Rugs', _('Rugs')),
            ('Photos', _('Photos')),
            ('Posters', _('Posters')),
            ('Tools', _('Tools')),
            ('Tools', _('Tools')),
            ('Fencing', _('Fencing')),
        ]),
        (('clothes', _('Clothes')), [
            ('Tops', _('Tops')),
            ('Bottoms', _('Bottoms')),
            ('Dress-Up', _('Dress-Up')),
            ('Headwear', _('Headwear')),
            ('Accessories', _('Accessories')),
            ('Socks', _('Socks')),
            ('Shoes', _('Shoes')),
            ('Bags', _('Bags')),
            ('Umbrellas', _('Umbrellas')),
        ]),
        (('critters', _('Critters')), [
            ('Insects', _('Insects')),
            ('Fish', _('Fish')),
        ]),
        (('other', _('Other')), [
            ('Music', _('Music')),
            ('Recipes', _('Recipes')),
            ('Fossils', _('Fossils')),
            ('Art', _('Art')),
            ('Other', _('Other')),
            ('Construction', _('Construction')),
        ]),
    ])
    TYPE_CHOICES = reduce(operator.add, CATEGORIES.values())
    i_type = models.PositiveIntegerField(_('Type'), choices=i_choices(TYPE_CHOICES), null=True)

    # todo check
    IN_VILLAGER_HOUSE_TYPES = [
        'Housewares',
        'Miscellaneous',
        'Wall-mounted',
        'Rugs',
        'Photos',
        'Posters',
        'Tools',
    ]

    ############################################################
    # Internal fields

    internal_id = models.TextField(null=True, unique=True)

############################################################
# Villager

class Villager(MagiModel):
    collection_name = 'villager'

    owner = models.ForeignKey(User, related_name='added_villagers')

    ############################################################
    # Images

    image = models.ImageField(_('Image'), upload_to=uploadItem('villager'), null=True)
    icon_image = models.ImageField(_('Icon'), upload_to=uploadItem('villager'), null=True)
    house_image = models.ImageField(_('House'), upload_to=uploadItem('villager'), null=True)

    ############################################################
    # Main fields

    name = models.CharField(_('Name'), max_length=100, unique=True, db_index=True)

    species = models.CharField(_('Species'), max_length=100, null=True)

    GENDER_CHOICES = (
        'Male',
        'Female',
        'Other',
    )
    i_gender = models.PositiveIntegerField(_('Gender'), choices=i_choices(GENDER_CHOICES), default=2)

    personality = models.CharField(_('Personality'), max_length=100, null=True)
    hobby = models.CharField(_('Hobby'), max_length=100, null=True)
    catchphrase = models.CharField(_('Catchphrase'), max_length=100, null=True)

    birthday = models.DateField(_('Birthday'), null=True)
    display_birthday = property(lambda _s: date_format(_s.birthday, format='MONTH_DAY_FORMAT', use_l10n=True))

    _to_style_verbose_name = lambda _s, _i=None: (u'{} ({})' if _i else u'{}').format(
        _('Favorite {thing}').format(thing=_('Style').lower()), _i)
    style1 = models.CharField(_to_style_verbose_name(1), null=True, max_length=100)
    style2 = models.CharField(_to_style_verbose_name(2), null=True, max_length=100)

    _to_color_verbose_name = lambda _s, _i=None: (u'{} ({})' if _i else u'{}').format(
        _('Favorite {thing}').format(thing=_('Color').lower()), _i)
    color1 = models.CharField(_to_color_verbose_name(1), null=True, max_length=100)
    color2 = models.CharField(_to_color_verbose_name(2), null=True, max_length=100)

    music = models.ForeignKey(Item, null=True, verbose_name=_('Song'), limit_choices_to={
        'i_type': Item.get_i('type', 'Music'),
    }, related_name='villagers_with_song')

    ############################################################
    # House details

    wallpaper = models.ForeignKey(Item, null=True, verbose_name=_('Wallpaper'), limit_choices_to={
        'i_type': Item.get_i('type', 'Wallpaper'),
    }, related_name='villagers_with_wallpaper')
    floor = models.ForeignKey(Item, null=True, verbose_name=_('Floor'), limit_choices_to={
        'i_type': Item.get_i('type', 'Floors'),
    }, related_name='villagers_with_floor')

    furnitures = models.ManyToManyField(Item, null=True, verbose_name=_('Furnitures'), limit_choices_to={
        'i_type__in': [
            Item.get_i('type', _type)
            for _type in Item.IN_VILLAGER_HOUSE_TYPES
        ],
    })

    ############################################################
    # Internal fields

    unique_entry_id = models.TextField(null=True, unique=True)
    filename = models.TextField(null=True)

    ############################################################
    # Views utils

    image_for_favorite_character = property(lambda _s: _s.icon_image_url)
    image_for_prefetched = property(lambda _s: _s.icon_image_url)

    ############################################################
    # Unicode

    def __unicode__(self):
        return self.name

    ############################################################
    # Meta

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
        return self.villager.icon_image

    def __unicode__(self):
        return unicode(self.villager)
