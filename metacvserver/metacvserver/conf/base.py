"""
Django settings for metacvserver project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['heymistertree.eu']

TEMPLATE_DEBUG = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sass_processor',
    'cv',
    'video',
    'themaintemplate',
    'analytical'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'metacvserver.urls'

WSGI_APPLICATION = 'metacvserver.wsgi.application'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'db',
        'NAME': 'metacvserver',
        'USER': 'monsieurarbre',
        'PASSWORD' : os.environ['POSTGRES_PASSWORD']
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = '/var/django/metacvserver_static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    '/var/django/metacvserver_compiledjs/',
    'common/'
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
)
MEDIA_ROOT = '/var/django/metacvserver_media/'
MEDIA_URL = '/media/'

SASS_PROCESSOR_INCLUDE_DIRS = (
    'common/',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
      'request': {
        'level': 'INFO',
        'class': 'logging.FileHandler',
        'filename':
          '/var/django/metacvserver_logs/request.log',
      },
      'security': {
        'level': 'INFO',
        'class': 'logging.FileHandler',
        'filename':
          '/var/django/metacvserver_logs/security.log',
      },
    },
    'loggers': {
      'django.request': {
        'handlers': ['request'],
        'level': 'DEBUG',
        'propagate': True,
      },
      'django.security': {
        'handlers': ['security'],
        'level': 'DEBUG',
        'propagate': True,
      },
    },
}

GOOGLE_ANALYTICS_PROPERTY_ID = os.environ['GOOGLE_ANALYTICS_KEY']
GOOGLE_ANALYTICS_SITE_SPEED = True

FIRST_NAME = "Florent"
SURNAME = "Pastor"
PUBLIC_EMAIL = "mistertree@openmailbox.org"
