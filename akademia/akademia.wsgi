import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'akademia.settings.akademia'
from akademia.wsgi import application
