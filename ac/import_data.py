import urllib2
from bs4 import BeautifulSoup
from magi import urls # for static images
from magi.utils import (
    get_default_owner,
    saveImageURLToModel,
)
from ac import models

VILLAGERS_URL = u'https://nookipedia.com/wiki/List_of_villagers'
IMAGES_BASE_URL = u'https://nookipedia.com'

def import_villagers(local=False, verbose=False, force_reload_images=False):
    owner = get_default_owner(models.User)

    if local:
        f = open('villagers.html', 'r')
        html = f.read()
        f.close()
    else:
        f = urllib2.urlopen(VILLAGERS_URL)
        html = f.read()
        f.close()
        f_save = open('villagers.html', 'w')
        f_save.write(html)
        f_save.close()
    soup = BeautifulSoup(html, features='html.parser')
    content = soup.find('div', { 'id': 'mw-content-text' })
    table = content.find('table')
    for tr in table.find('tbody').find_all('tr'):
        tds = tr.find_all(['td', 'th'])
        if not tds or len(tds) < 14:
            continue
        is_in_acnh = bool(tds[13].find('img'))
        if not is_in_acnh:
            continue
        image = tds[0].find('img').get('src')
        name = tds[1].find('a').text.strip()
        species = tds[3].text.strip()
        gender = tds[4].text.strip()
        personality = tds[5].find('a').text.strip()

        if verbose:
            print name

        try:
            villager = models.Villager.objects.filter(name=name)[0]
        except IndexError:
            villager = models.Villager.objects.create(owner=owner, name=name)

        if not villager.image or force_reload_images:
            image_url = u'{}{}'.format(IMAGES_BASE_URL, image)
            saveImageURLToModel(villager, 'image', url=image_url)

        villager.species = species
        villager.personality = personality

        try:
            i_gender = models.Villager.get_i('gender', gender)
        except KeyError:
            i_gender = models.Villager.get_i('gender', 'Other')
        villager.i_gender = i_gender

        villager.save()

def import_data(verbose=False, local=False, to_import=None, force_reload_images=False):
    import_villagers(local=local, verbose=verbose, force_reload_images=force_reload_images)
