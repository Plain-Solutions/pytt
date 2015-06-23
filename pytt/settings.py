import ConfigParser
import os
from django.core.management import call_command

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEFAULT_CHARSET = 'utf-8'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
ROOT_URLCONF = 'pytt.urls'
WSGI_APPLICATION = 'pytt.wsgi.application'
APPEND_SLASH = True
UPDATE_INTERVAL = 3 * 60 * 60
# Contains all the crucial secured params for the project
PROP_FILE = 'config.properties'

config = ConfigParser.ConfigParser()
config.read(PROP_FILE)

SECRET_KEY = config.get('DJANGO', 'secret_key')

# This is used for memcached to store data

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'pytt'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'pytt',
        'USER': config.get('DB', 'user'),
        'PASSWORD': config.get('DB', 'password'),
        'HOST': config.get('DB', 'host'),
        'PORT': config.get('DB', 'port')
    }
}

REST_FRAMEWORK = {
    'UNICODE_JSON': True,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'COMPACT_JSON': True
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(process)d [%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }},
    'handlers': {
        'info': {
            'mode': 'w',
            'formatter': 'verbose',
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './info.log',
            'maxBytes': 1048576,
            'backupCount': 3,
        },
        'error': {
            'mode': 'w',
            'formatter': 'verbose',
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './error.log',
            'maxBytes': 1048576,
            'backupCount': 3,
        }
    },
    'root': {
        'handlers': ['info', 'error'],
        'formatter': 'verbose',
        'level': 'DEBUG'
    }
}
