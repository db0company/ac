# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.db.models import Q
from magi.management.commands.populate_staffconfigurations import create
from magi import models as magi_models

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Set up defaults for existing configurations

        magi_models.StaffConfiguration.objects.filter(key='about_image').filter(Q(value__isnull=True) | Q(value='')).update(value='tom_nook.png')
        magi_models.StaffConfiguration.objects.filter(key='about_the_website', i_language='en').filter(Q(value__isnull=True) | Q(value='')).update(value="""
Welcome to AC!

AC is a community for Animal Crossing players.

- Make new friends
- Share your photos and creations with the community
- Share your island details and villagers with everyone
- and more
""")
        magi_models.StaffConfiguration.objects.filter(key='about_us', i_language='en').filter(Q(value__isnull=True) | Q(value='')).update(value="""
Seeing everyone share their creations on Animal Crossing: New Horizons was what motivated me to start this community. Your creativity is just so impressive!

With this community, I hope to create a safe space for players of all ages and backrgound, to discuss Animal Crossing and all the cuteness that comes with it.

I hope you'll enjoy your stay. Please let me know if you have feedback to share and suggestions.
""")
        magi_models.StaffConfiguration.objects.filter(key='get_started', i_language='en').filter(Q(value__isnull=True) | Q(value='')).update(value=u"""
## **Thanks for joining AC ❤️**

Let's finish setting up your profile!

#### **Who are the villagers who live on your island?**

1. Go through the list of villagers and look for them
    - 💡 You can use the side bar to search!
2. Click "Add to your island!"

        Once you're done, check [your profile](/me/)!

You can find more options to personalize your profile in your [settings](/settings/).
""")
