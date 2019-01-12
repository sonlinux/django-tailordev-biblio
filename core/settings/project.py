# coding=utf-8

"""Project level settings.

Adjust these values as needed but don't commit passwords etc. to any public
repository!
"""

from django.utils.translation import ugettext_lazy as _
from .contrib import *  # noqa

# Project apps
INSTALLED_APPS += (
    'td_biblio',
)

# Set languages which want to be translated
LANGUAGES = (
    ('en', _('English')),
)

VALID_DOMAIN = [
    '0.0.0.0',
]

PIPELINE = {
    'STYLESHEETS': {
        'td-biblio-base': {
            'source_filenames': {
                'css/styles.css',
            },
            'output_filename': 'css/styles.css',
            'extra_content': {
                'media': 'screen, projection',
            }
        }
    },
    'JAVASCRIPT': {

    }
}
# library needs to be added to path below
REQUIRE_JS_PATH = '/static/js/libs/requirejs-2.3.5/require.js'

GRUNT_MODULES = {
    'base-view': {
        'main': 'js/app',
        'optimized': 'js/optimized.js',
    }
}
