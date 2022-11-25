"""
Django settings for renskin project.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/

For production settings see
https://docs.djangoproject.com/en/dev/howto/deployment/checklist/
"""
from ddhldap.settings import * # noqa
import logging
import getpass

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

PROJECT_NAME = 'renskin'
PROJECT_TITLE = 'Renaissance Skin'

# -----------------------------------------------------------------------------
# Core Settings
# https://docs.djangoproject.com/en/dev/ref/settings/#id6
# -----------------------------------------------------------------------------

ADMINS = ()
MANAGERS = ADMINS

ALLOWED_HOSTS = []

# https://docs.djangoproject.com/en/dev/ref/settings/#caches
# https://docs.djangoproject.com/en/dev/topics/cache/
# http://redis.io/topics/lru-cache
# http://niwibe.github.io/django-redis/
CACHE_REDIS_DATABASE = '0'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/' + CACHE_REDIS_DATABASE,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True
        }
    }
}

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ddhldap',
    'compressor',

    'taggit',
)


INSTALLED_APPS += (
    'wagtail.core',
    'wagtail.admin',
    'wagtail.documents',
    'wagtail.snippets',
    'wagtail.users',
    'wagtail.images',
    'wagtail.embeds',
    'wagtail.search',
    'wagtail.contrib.redirects',
    'wagtail.contrib.forms',
    'wagtail.sites',
    'wagtail.contrib.routable_page',
)


INSTALLED_APPS += (
    # your project apps here
    'cms',
    # 'wagtail.contrib.modeladmin',  # for wagtailmenus
    # 'wagtailmenus',
)

INTERNAL_IPS = ('127.0.0.1', )

# https://docs.djangoproject.com/en/dev/topics/logging/

LOGGING_ROOT = os.path.join(BASE_DIR, 'logs')
LOGGING_LEVEL = logging.WARN

if not os.path.exists(LOGGING_ROOT):
    os.makedirs(LOGGING_ROOT)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(levelname)s %(asctime)s %(module)s '
                       '%(process)d %(thread)d %(message)s')
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'django.log'),
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins'],
            'level': LOGGING_LEVEL,
            'propagate': True
        },
        'django_auth_ldap': {
            'handlers': ['file'],
            'level': LOGGING_LEVEL,
            'propagate': True
        },
        'renskin': {
            'handlers': ['file'],
            'level': LOGGING_LEVEL,
            'propagate': True
        },
    }
}


MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',


    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = PROJECT_NAME + '.urls'

WAGTAIL_SITE_NAME = PROJECT_TITLE

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                # 'wagtailmenus.context_processors.wagtailmenus',
            ],
            'debug': False,
        },
    },
]

# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = False
USE_TZ = True

WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'


# -----------------------------------------------------------------------------
# Authentication
# https://docs.djangoproject.com/en/dev/ref/settings/#auth
# https://scm.cch.kcl.ac.uk/hg/ddhldap-django
# -----------------------------------------------------------------------------

AUTH_LDAP_REQUIRE_GROUP = 'cn=renskin,' + LDAP_BASE_OU
AUTH_LDAP_USER_FLAGS_BY_GROUP['is_staff'] = 'cn=renskin,' + LDAP_BASE_OU  # noqa


# -----------------------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
# https://docs.djangoproject.com/en/dev/ref/settings/#static-files
# -----------------------------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL.strip('/'))

if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'assets'),)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# STATICFILES_STORAGE = 'require.storage.OptimizedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL.strip('/'))

if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

if not os.path.exists(os.path.join(MEDIA_ROOT, 'original_images')):
    print('WARNING: the media folder is now under /media instead of /static/media, did forget to move the content?')

# -----------------------------------------------------------------------------
# EMAIL SETTINGS
# -----------------------------------------------------------------------------

EMAIL_HOST = 'smtp.kcl.ac.uk'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'noreply@kcl.ac.uk'
# Sender of error messages to ADMINS and MANAGERS
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_SUBJECT_PREFIX = '[Django {}] '.format(PROJECT_NAME)

# -----------------------------------------------------------------------------
# Sessions
# https://docs.djangoproject.com/en/1.8/ref/settings/#sessions
# -----------------------------------------------------------------------------

SESSION_COOKIE_SECURE = True

# -----------------------------------------------------------------------------
# Installed Applications Settings
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Django Compressor
# http://django-compressor.readthedocs.org/en/latest/
# -----------------------------------------------------------------------------

COMPRESS_ENABLED = True

COMPRESS_CSS_FILTERS = [
    # CSS minimizer
    'compressor.filters.cssmin.CSSMinFilter'
]

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# -----------------------------------------------------------------------------
# Django Grappelli
# http://django-grappelli.readthedocs.org/en/latest/
# -----------------------------------------------------------------------------

GRAPPELLI_ADMIN_TITLE = PROJECT_TITLE

# -----------------------------------------------------------------------------
# Django-Require
# https://github.com/etianen/django-require
# -----------------------------------------------------------------------------

# # The baseUrl to pass to the r.js optimizer, relative to STATIC_ROOT.
# REQUIRE_BASE_URL = 'js'
#
# # The name of a build profile to use for your project, relative to
# # REQUIRE_BASE_URL. A sensible value would be 'app.build.js'.
# # Leave blank to use the built-in default build profile. Set to False to
# # disable running the default profile (e.g. if only using it to build
# # Standalone Modules)
# REQUIRE_BUILD_PROFILE = False
#
# # The name of the require.js script used by your project, relative to
# # REQUIRE_BASE_URL.
# REQUIRE_JS = '../vendor/requirejs/require.js'
#
# # A dictionary of standalone modules to build with almond.js.
# # See the section on Standalone Modules, below.
# REQUIRE_STANDALONE_MODULES = {
#     'config': {
#         # Where to output the built module, relative to REQUIRE_BASE_URL.
#         'out': 'config-built.js',
#
#         # Optional: A build profile used to build this standalone module.
#         'build_profile': 'config.build.js',
#     }
# }
#
# # Whether to run django-require in debug mode.
# REQUIRE_DEBUG = DEBUG
#
# # A tuple of files to exclude from the compilation result of r.js.
# REQUIRE_EXCLUDE = ('build.txt', )
#
# # The execution environment in which to run r.js: auto, node or rhino.
# # auto will autodetect the environment and make use of node if available and
# # rhino if not.
# REQUIRE_ENVIRONMENT = 'node'

# -----------------------------------------------------------------------------
# FABRIC
# -----------------------------------------------------------------------------

FABRIC_USER = getpass.getuser()

ITEMS_PER_PAGE = 10

# -----------------------------------------------------------------------------
# GLOBALS FOR JS
# -----------------------------------------------------------------------------

WAGTAILSEARCH_RESULTS_TEMPLATE = 'cms/search_results.html'  # Really wagtail?

# the slug of the Visible Skin exhibition landing page
VISIBLE_SKIN_SLUG = 'visibleskin'
