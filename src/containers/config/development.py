# Development configuration
from flask.ext.babel import lazy_gettext as _

DEBUG = True
DEBUG_TOOLBAR = True

ASSETS_AUTO_BUILD = False

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres@127.0.0.1:5432/containers'
SQLALCHEMY_TESTDATABASE_URI = 'postgresql+psycopg2://postgres@127.0.0.1:5432/containers_test'

BABEL_DEFAULT_LOCALE = 'ru'
LANGUAGES = {
    'en': _('English'),
    'ru': _('Russian')
}
