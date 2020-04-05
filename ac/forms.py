from django import forms
from django.conf import settings as django_settings
from django.db.models.fields import BLANK_CHOICE_DASH
from magi.forms import (
    AccountForm as _AccountForm,
    MagiFiltersForm,
)
from ac import models

class AccountForm(_AccountForm):
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for field_name in ['level', 'nickname']:
            if field_name in self.fields:
                del(self.fields[field_name])
        if 'photo' in self.fields:
            if self.is_creating:
                del(self.fields['photo'])
            else:
                self.fields['photo'].queryset = self.fields['photo'].queryset.filter(owner=self.request.user)

class VillagerFilterForm(MagiFiltersForm):
    search_fields = ['name']

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
