import logging
import os
import sys

import dj_database_url
import sentry_sdk
from celery.schedules import crontab
from sentry_sdk.integrations.django import DjangoIntegration
from dotenv import load_dotenv

from contributors.utils import misc

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Logging setup
logging.basicConfig(
    level=logging.DEBUG,
    filename=os.path.join(BASE_DIR, 'logs/events.log'),
    filemode='w',
    format='{asctime} - {levelname} - {message}',
    datefmt='%H:%M:%S',
    style='{',
)

SECRET_KEY = misc.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'true').lower() in {'yes', '1', 'true'}

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    '.herokuapp.com',
    '.railway.app',
    '.hexlet.io',
    '0.0.0.0',
]

# Add render hosts to allowed for deploy

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


INSTALLED_APPS = [
    'contributors.apps.CustomAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'contributors.apps.ContributorsConfig',
    'auth.apps.AuthConfig',
    'crispy_forms',
    "crispy_bootstrap5",
    'django_extensions',
    'mathfilters',
    'django_filters',
    'django.contrib.sitemaps'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'config.middlewares.GlobalHostRateLimitMiddleware'
]


# Django Debug Toolbar Settings
if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    INTERNAL_IPS = [
        '127.0.0.1',
        'localhost',
    ]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'contributors.context_processors.general_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Authentication

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'auth.backends.GitHubBackend',
]

AUTH_USER_MODEL = 'custom_auth.SiteUser'

LOGIN_REDIRECT_URL = 'contributors:home'

LOGOUT_REDIRECT_URL = 'contributors:home'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'postgres'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'password'),
        'HOST': os.getenv('POSTGRES_HOST', 'postgres'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    },
}

SQLITE_SETTINGS = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}

if os.getenv('DB_ENGINE') == 'SQLite':
    DATABASES['default'] = SQLITE_SETTINGS

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

CONN_MAX_AGE = 500

# Use the DATABASE_URL environment variable
# https://pypi.org/project/dj-database-url/

if os.getenv('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(conn_max_age=CONN_MAX_AGE)

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-gb'

LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Russian'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Project specific settings

PROJECT_NAME = 'Hexlet Friends'

GITHUB_AUTH_TOKEN = os.getenv('GITHUB_AUTH_TOKEN')

GITHUB_APP_ID = os.getenv('GITHUB_APP_ID')
GITHUB_APP_ORG_OWNER = os.getenv('GITHUB_APP_ORG_OWNER')
GITHUB_APP_PRIVATE_KEY = os.getenv('GITHUB_APP_PRIVATE_KEY')

GITHUB_AUTH_CLIENT_ID = os.getenv('GITHUB_AUTH_CLIENT_ID')
GITHUB_AUTH_CLIENT_SECRET = os.getenv('GITHUB_AUTH_CLIENT_SECRET')

GITHUB_WEBHOOK_TOKEN = os.getenv('GITHUB_WEBHOOK_TOKEN')

GTM_ID = os.environ.get('GTM_ID')
YANDEX_VERIFICATION = os.environ.get('YANDEX_VERIFICATION')

TEXT_COLUMNS = ('name', 'organization', 'project', 'login')

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

SENTRY_SAMPLE_RATE = 0.01

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=SENTRY_SAMPLE_RATE,
    # To set a uniform sample rate
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production,
    profiles_sample_rate=SENTRY_SAMPLE_RATE,
)

GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}


""" DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
} """


CACHES = {
    'default': {
        'BACKEND': 'django_bmemcached.memcached.BMemcached',
        'LOCATION': os.environ.get('CACHE_LOCATION', '').split(','),
        'OPTIONS': {
            'username': os.environ.get('CACHE_USERNAME', ''),
            'password': os.environ.get('CACHE_PASSWORD', '')
        }
    }
}

if 'test' in sys.argv:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

SITE_ID = 1

# Just broker URL, no result backend needed
CELERY_BROKER_URL = os.getenv('BROKER_URL', 'amqp://guest:guest@172.17.0.1:5672//')
CELERY_RESULT_BACKEND = None
CELERY_IGNORE_RESULT = True

CELERY_BEAT_SCHEDULE = {
    'sync-github-repositories': {
        'task': 'contributors.tasks.sync_github_data',
        'schedule': crontab(hour='*/6'),
        'options': {
            'expires': 3600,
            'time_limit': 3600,
        }
    },
}

HOSTNAME_BLACKLIST = []

RATELIMIT_REQUESTS = int(os.getenv('RATELIMIT_REQUESTS', 1000))
RATELIMIT_TIMEFRAME = int(os.getenv('RATELIMIT_TIMEFRAME', 3600))
