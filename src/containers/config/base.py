# Base configuration
import os

from flask.ext.babel import lazy_gettext as _


PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = os.path.abspath(PROJECT_DIR)
PROJECT_ROOT = os.path.dirname(PROJECT_DIR)

DEBUG = True
DEBUG_TOOLBAR = False
DEBUG_TB_INTERCEPT_REDIRECTS = False

SECRET_KEY = 'jwf1n_e#c(fb=3rj==1sv0-kc=wpghacy_@zi-%n-nso(olh=j'

ASSETS_CACHE = os.path.join(PROJECT_ROOT, 'tmp', '.webassets-cache')

BLUEPRINTS = [
]

BABEL_DEFAULT_LOCALE = 'ru'
LANGUAGES = {
    'en': _('English'),
    'ru': _('Russian'),
}

COLLECT_STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public', 'static')
COLLECT_STORAGE = 'flask.ext.collect.storage.file'
