from akademia.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'database.sqlite3'),
    },
}

DEBUG = True
TEMPLATE_DEBUG = True
