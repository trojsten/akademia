import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'akademia.settings.klub'
from akademia.wsgi import application
