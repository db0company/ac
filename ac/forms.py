from django import forms
from django.conf import settings as django_settings
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.safestring import mark_safe
from magi.forms import (
    AccountForm as _AccountForm,
    MagiFiltersForm,
)
from magi.utils import (
    HTMLAlert
)
from ac import models

class AccountForm(_AccountForm):
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for field_name in ['level', 'nickname']:
            if field_name in self.fields:
                del(self.fields[field_name])
        if 'photo' in self.fields:
            self.fields['photo'].queryset = self.fields['photo'].queryset.filter(owner=self.request.user)
        if 'best_friend' in self.fields:
            if self.is_creating:
                del(self.fields['best_friend'])
            else:
                self.fields['best_friend'].queryset = self.fields['best_friend'].queryset.filter(account=self.instance)
        if self.is_creating and 'title' in self.fields: # not simple
            self.afterfields = mark_safe(HTMLAlert(type='info', message=(
                'You can edit your island later to add your cover photo and best friend.')))

class VillagerFilterForm(MagiFiltersForm):
    search_fields = ['name', 'species']

    species = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [
        (_k, _k) for _k in getattr(django_settings, 'SPECIES_CHOICES', [])])
    personality = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [
        (_k, _k) for _k in getattr(django_settings, 'PERSONALITY_CHOICES', [])])

    class Meta(MagiFiltersForm.Meta):
        model = models.Villager
        fields = [
            'search',
            'species',
            'i_gender',
            'personality',
        ]
