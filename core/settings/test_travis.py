# -*- coding: utf-8 -*-
__author__ = 'Alison Mukoma <sonlinux>'

from .test import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'test_db',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        # Set to empty string for default.
        'PORT': '',
    }
}

MEDIA_ROOT = '/tmp/media'
STATIC_ROOT = '/tmp/static'
