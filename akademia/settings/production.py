from __future__ import absolute_import
from akademia.settings.common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'akademia',
        'USER': 'akademia',
    }
}

STATIC_ROOT = '/var/www/akademia/static/'
MEDIA_ROOT = '/var/www/akademia/media/'
MEDIA_URL = '/media/'

try:
    from akademia.settings.local import *
except ImportError:
    pass
