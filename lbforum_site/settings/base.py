"""
Django settings for lbforum_site project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys

from django.conf.global_settings import STATICFILES_FINDERS
from django.conf.global_settings import AUTHENTICATION_BACKENDS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PRJ_ROOT = os.path.join(BASE_DIR, '..')

VENDOR_DIR = os.path.join(PRJ_ROOT, 'vendor')
sys.path.insert(0, os.path.join(VENDOR_DIR, 'lbforum'))
sys.path.insert(0, os.path.join(VENDOR_DIR, 'lbutils'))
sys.path.insert(0, os.path.join(VENDOR_DIR, 'django-lbattachment'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@hq__xnkji!*&eetd=39q4e=+(2)a0!!-(0i7&g1+1^og#yu@('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'lbforum_site',

    'el_pagination',
    'easy_thumbnails',
    'constance',
    'constance.backends.database',
    'djangobower',
    'allauth',
    'allauth.account',
    'captcha',
    'rest_framework',

    'lbforum',
    'lbattachment',
    'lbutils',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'lbforum_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lbforum_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PRJ_ROOT, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGES = (
    ('en', ('English')),
    ('zh-hans', ('中文简体')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PRJ_ROOT, 'collectedstatic')

HOST_URL = ''
MEDIA_URL_ = '/media/'
MEDIA_URL = HOST_URL + MEDIA_URL_
MEDIA_ROOT = os.path.join(PRJ_ROOT, 'media')

LBFORUM_TITLE = "论坛首页"
LBFORUM_SUB_TITLE = ""

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'forbidden_words': ('', 'Forbidden words', str),
}

BOWER_COMPONENTS_ROOT = PRJ_ROOT

BOWER_INSTALLED_APPS = (
    'jquery#1.12',
    'markitup#1.1.14',
    'mediaelement#2.22.0',
    'blueimp-file-upload#9.12.5',
)

STATICFILES_FINDERS += (('djangobower.finders.BowerFinder'),)
AUTHENTICATION_BACKENDS += (('allauth.account.auth_backends.AuthenticationBackend'),)

SITE_ID = 1

ACCOUNT_FORMS = {'signup': 'lbforum_site.forms.SignupForm'}
ACCOUNT_LOGOUT_ON_GET = True

SIGNUP_URL = '/accounts/signup/'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/'
CHANGE_PASSWORD_URL = '/accounts/password/change/'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'PAGE_SIZE': 20
}
