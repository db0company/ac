from magi.tools import generateSettings
from ac import models

def generate_settings():
    generateSettings({
        'PERSONALITY_CHOICES': sorted(list(
            models.Villager.objects.order_by('personality').values_list(
                'personality', flat=True).distinct())),
        'SPECIES_CHOICES': sorted(list(
            models.Villager.objects.order_by('species').values_list(
                'species', flat=True).distinct())),
        # todo colors and styles
    })
