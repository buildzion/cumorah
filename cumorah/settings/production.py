from .base import *

import dj_database_url

DEBUG = False

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", '*').split(',')

SECRET_KEY = os.environ.get('SECRET_KEY', "This isn't a good secret key default value, you should set one in the environment")

if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config()
    }


LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

try:
    from .local import *
except ImportError:
    pass
