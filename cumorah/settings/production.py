import os

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
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        }
    },
    'loggers': {
        'root': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.request': {
            'handlers': ["mail_admins"],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

if os.environ.get("DOCKER_TEMPLATE_DIR"):
    TEMPLATES[0]['DIRS'].insert(0, os.environ.get("DOCKER_TEMPLATE_DIR"))


try:
    from local_settings import *
except ImportError:
    pass
