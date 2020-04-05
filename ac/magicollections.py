from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from magi.magicollections import (
    MagiCollection,
    MainItemCollection,
    UserCollection as _UserCollection,
    ActivityCollection as _ActivityCollection,
    AccountCollection as _AccountCollection,
    DonateCollection as _DonateCollection,
    BadgeCollection as _BadgeCollection,
    StaffConfigurationCollection as _StaffConfigurationCollection,
)
from magi.utils import (
    justReturn,
)
from magi.forms import get_account_simple_form
from ac import models, forms

############################################################
# Activity Collection

class ActivityCollection(_ActivityCollection):
    title = _('Post')
    plural_title = _('Posts')
    navbar_link = True

############################################################
# StaffConfiguration Collection

class StaffConfigurationCollection(_StaffConfigurationCollection):
    enabled = True

############################################################
# Donate Collection

class DonateCollection(_DonateCollection):
    enabled = True

############################################################
# Badge Collection

class BadgeCollection(_BadgeCollection):
    enabled = True

############################################################
# User Collection

class UserCollection(_UserCollection):
    navbar_link = True
    icon = 'users'

    class ListView(_UserCollection.ListView):
        pass

############################################################
# Account Collection

class AccountCollection(_AccountCollection):
    title = _('Island')
    plural_title = _('Islands')
    navbar_link = False
    form_class = forms.AccountForm

    fields_icons = _AccountCollection.fields_icons
    fields_icons.update({
        'name': 'map',
        'character_name': 'idol',
        'native_fruit': 'food-like',
        'title': 'hashtag',
        'message': 'author',
    })

    class ListView(_AccountCollection.ListView):
        def get_page_title(self):
            return _('Islands')

    class AddView(_AccountCollection.AddView):
        simpler_form = get_account_simple_form(forms.AccountForm, simple_fields=[
            'name', 'character_name', 'friend_id',
        ])

############################################################
# Villager collections

def to_AddedVillagerCollection(cls):
    class _AddedVillagerCollection(cls):
        add_sentence = 'Add villager to island'
        plural_title = 'Villagers'

        class AddView(cls.AddView):
            quick_add_to_collection = justReturn(True)
            unique_per_owner = True

        class ListView(cls.ListView):
            show_items_names = True

    return _AddedVillagerCollection

class VillagerCollection(MainItemCollection):
    queryset = models.Villager.objects.all()
    navbar_link = False
    icon = 'chibi'
    collectible = models.AddedVillager

    fields_icons = {
        'name': 'id',
        'species': 'chibi',
        'gender': 'idolized',
        'personality': 'about',
    }

    def collectible_to_class(self, model_class):
        return to_AddedVillagerCollection(super(VillagerCollection, self).collectible_to_class(model_class))

    class ListView(MainItemCollection.ListView):
        filter_form = forms.VillagerFilterForm
        show_items_names = True
