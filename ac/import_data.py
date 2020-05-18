import urllib2
from bs4 import BeautifulSoup
from magi import urls # for static images
from magi.utils import (
    get_default_owner,
    saveImageURLToModel,
)
from magi.import_data import (
    import_from_sheet,
)
from ac import models

SPREADSHEET_ID = '1mydFUg9AK21Ilb2twxhF9Wjqsged50L2nezf9PwDJ6Q'

IMPORT_CONFIGURATION = {
    'Villagers': {
        'model': models.Villager,
        'unique_fields': [
            'name'
        ],
        'mapping': {
            'Name': 'name',
            'Icon Image': 'icon_image',
            'House Image': 'house_image',
            'Species': 'species',
            'Gender': 'i_gender',
            'Personality': 'personality',
            'Hobby': 'hobby',
            'Birthday': lambda v: ('birthday', u'2020-{}'.format(u'-'.join(v.split('/')))),
            'Catchphrase': 'catchphrase',
            'Color 1': 'color1',
            'Color 2': 'color2',
            'Flooring': lambda v: ('floor', models.Item, { 'name': v }, {
                'i_type': models.Item.get_i('type', 'Floors'),
            }),
            'Wallpaper': lambda v: ('wallpaper', models.Item, { 'name': v }, {
                'i_type': models.Item.get_i('type', 'Wallpaper'),
            }),
            'Unique Entry ID': 'unique_entry_id',
            'Style 1': 'style1',
            'Style 2': 'style2',
            'Filename': 'filename',
            'Furniture List': lambda v: ('furnitures', [
                models.Item.objects.get_or_create(internal_id=_id, defaults={ 'owner': get_default_owner(models.User) })[0]
                for _id in v.split(',')
            ]),
            'Favorite Song': lambda v: ('music', models.Item, { 'name': v }, {
                'i_type': models.Item.get_i('type', 'Music'),
            }),
        },
    },
}

#################################

VILLAGERS_URL = u'https://nookipedia.com/wiki/List_of_villagers'
IMAGES_BASE_URL = u'https://nookipedia.com'

def import_villagers(local=False, verbose=False, force_reload_images=False, load_on_not_found_local=True):
    local_file_name = 'nookpedia_villagers.html'
    owner = get_default_owner(models.User)
    html = None

    if local:
        if load_on_not_found_local:
            try: f = open(local_file_name, 'r')
            except IOError: f = None
        else:
            f = open(local_file_name, 'r')
        if f:
            html = f.read()
            f.close()
    if not html:
        f = urllib2.urlopen(VILLAGERS_URL)
        html = f.read()
        f.close()
        f_save = open('nookpedia_villagers.html', 'w')
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
    if not to_import or 'nookpedia_villagers' in to_import:
        print 'Import villagers from Nookpedia wiki (3D models)'
        import_villagers(local=local, verbose=verbose, force_reload_images=force_reload_images)
    print 'Import from sheets'
    import_from_sheet(
        SPREADSHEET_ID, IMPORT_CONFIGURATION, local=local, verbose=verbose,
        to_import=to_import, force_reload_images=force_reload_images,
    )
