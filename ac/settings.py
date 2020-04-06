# -*- coding: utf-8 -*-
import datetime, pytz
from django.conf import settings as django_settings
from magi.default_settings import (
    DEFAULT_ACTIVITY_TAGS,
    DEFAULT_ENABLED_PAGES,
    DEFAULT_ENABLED_NAVBAR_LISTS,
)
from ac import models

# Configure and personalize your website here.

SITE_NAME = 'AC'
SITE_DESCRIPTION = 'Make friends on Animal Crossing: New Horizons!'
SITE_URL = 'https://ac.db0.company/'
SITE_IMAGE = 'ac.png'
SITE_LOGO_WHEN_LOGGED_IN = 'ac_mini_logo.png'
SITE_NAV_LOGO = 'ac_mini_logo.png'
SITE_STATIC_URL = '//i-ac.db0.company/'
GAME_NAME = 'Animal Crossing: New Horizons'
DISQUS_SHORTNAME = 'ac-db0'
TWITTER_HANDLE = 'magicircles2'
GOOGLE_ANALYTICS = 'UA-96550529-2'
ACCOUNT_MODEL = models.Account
SHOW_TOTAL_ACCOUNTS = False
COLOR = '#03A179'
SECONDARY_COLOR = '#81D5EF'
ACCENT_COLOR = '#FFE34C'
FEEDBACK_FORM = 'https://forms.gle/QgEBXXSVfh8K2fSn9'

HASHTAGS = ['AnimalCrossing', 'ACNH']

LAUNCH_DATE = datetime.datetime(2019, 04, 05, 0, 0, 0, tzinfo=pytz.UTC)

GAME_DESCRIPTION = u"""
Escape to a deserted island and create your own paradise as you explore, create, and customize in the Animal Crossing: New Horizons game. Your island getaway has a wealth of natural resources that can be used to craft everything from tools to creature comforts. You can hunt down insects at the crack of dawn, decorate your paradise throughout the day, or enjoy sunset on the beach while fishing in the ocean. The time of day and season match real life, so each day on your island is a chance to check in and find new surprises all year round.
"""
GAME_URL = 'https://www.nintendo.com/games/detail/animal-crossing-new-horizons-switch/'

GITHUB_REPOSITORY = ('db0company', 'ac')

ACTIVITY_TAGS = DEFAULT_ACTIVITY_TAGS + [
    ('tips', 'Tips&Tricks'),
    ('photo', 'Photo'),
    ('download-design', 'Design to download'),
    ('outfit', 'Outfit'),
    ('craft', 'Craft'),
    ('neighboors', 'Neighboors'),
    ('home-design', 'Home design'),
    ('outdoor-design', 'Outdoor design'),
]
MINIMUM_LIKES_POPULAR = 0

BACKGROUNDS = [
    {
        'id': 1,
        'image': 'backgrounds/pattern.png',
        'name': 'Pattern',
    },
    {
        'id': 2,
        'image': 'backgrounds/tomnook.png',
        'name': 'Tom Nook',
    },
    {
        'id': 3,
        'image': 'backgrounds/bright_pattern.png',
        'name': 'Bright pattern',
    },
    {
        'id': 4,
        'image': 'backgrounds/grocery.png',
        'name': 'Grocery',
    },
]

DONATE_IMAGE = 'donate.png'
ABOUT_PHOTO = 'deby.png'
CORNER_POPUP_IMAGE = 'tom_nook.png'

FAVORITE_CHARACTERS_MODEL = models.Villager

USER_COLORS = [
    ('red', 'Red', 'red', '#ff4d5d'),
    ('orange', 'Orange', 'orange', '#ffb054'),
    ('yellow', 'Yellow', 'yellow', '#FFD34E'),
    ('green', 'Green', 'green', '#54ff79'),
    ('blue', 'Blue', 'blue', '#54b5ff'),
]

FIRST_COLLECTION = 'addedvillager'

ENABLED_PAGES = DEFAULT_ENABLED_PAGES

ENABLED_PAGES['login']['navbar_link_list'] = None
ENABLED_PAGES['signup']['navbar_link_list'] = None
ENABLED_PAGES['user']['navbar_link_list'] = None

ENABLED_NAVBAR_LISTS = DEFAULT_ENABLED_NAVBAR_LISTS
ENABLED_NAVBAR_LISTS['you']['icon'] = 'settings'
ENABLED_NAVBAR_LISTS['you']['title'] = ''
