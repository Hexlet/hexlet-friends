import logging
import os
from pathlib import Path
from typing import (List, Any, Dict, Tuple)

import dj_database_url
import environ

env = environ.Env()

BASE_DIR: Path = Path(__file__).parents[2]  # hexlet-friends/..
CONN_MAX_AGE: int = 500
ROOT_URLCONF: str = 'config.urls'
AUTH_USER_MODEL: str = 'custom_auth.SiteUser'
LOGIN_REDIRECT_URL: str = 'contributors:home'
LOGOUT_REDIRECT_URL: str = 'contributors:home'
DEFAULT_AUTO_FIELD: str = 'django.db.models.AutoField'

PROJECT_NAME: str = env.str('PROJECT_NAME', 'Hexlet Friends')

# Logging setup
# region
logging.basicConfig(
    level=logging.INFO,
    filename=BASE_DIR / 'logs' / 'events.log',
    filemode='w',
    format='{asctime} - {levelname} - {message}',
    datefmt='%H:%M:%S',
    style='{',
)
# endregion

SECRET_KEY = env.str('SECRET_KEY', '')
WSGI_APPLICATION: str = 'config.wsgi.application'
DEBUG: bool = False
SECURE_PROXY_SSL_HEADER: Tuple[str, str] = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT: bool = True

ALLOWED_HOSTS: List[str] = [
    '.herokuapp.com',
    '.hexlet.io',
]

# Applications
# region
DJANGO_APPS: List[str] = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
REQUIREMENTS_APPS: List[str] = [
    'crispy_forms',
]

PROJECT_APPS: List[str] = [
    'auth.apps.AuthConfig',
    'contributors.apps.CustomAdminConfig',
    'contributors.apps.ContributorsConfig',
]
INSTALLED_APPS: List[str] = [
    *DJANGO_APPS,
    *REQUIREMENTS_APPS,
    *PROJECT_APPS,
]
# endregion

# Middleware
# region
MIDDLEWARE: List[str] = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# endregion

# Templates
# region
TEMPLATES: List[Dict[str, Any]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
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

# Authentication
# region
AUTHENTICATION_BACKENDS: List[str] = [
    'django.contrib.auth.backends.ModelBackend',
    'auth.backends.GitHubBackend',
]

# endregion

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES: Dict[str, Dict[str, Any]] = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('POSTGRES_DB', 'postgres'),
        'USER': env.str('POSTGRES_USER', 'postgres'),
        'PASSWORD': env.str('POSTGRES_PASSWORD', 'password'),
        'HOST': env.str('POSTGRES_HOST', 'postgres'),
        'PORT': env.str('POSTGRES_PORT', '5432'),
    },
}

SQLITE_SETTINGS = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}

if os.getenv('DB_ENGINE') == 'SQLite':
    DATABASES['default'] = SQLITE_SETTINGS

# Use the DATABASE_URL environment variable
# https://pypi.org/project/dj-database-url/
if env.str('DATABASE_URL', ''):
    DATABASES['default'] = dj_database_url.config(conn_max_age=CONN_MAX_AGE)

# Password validation
# region
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS: List[Dict[str, Tuple[str, str]]] = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]
# endregion


# Internationalization
# region
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE: str = 'ru-ru'
LANGUAGES: List[Tuple[str, str]] = [
    ('en', 'English'),
    ('ru', 'Russian'),
]
LOCALE_PATHS: List[Path] = [
    BASE_DIR / 'locale',
]

TIME_ZONE: str = 'Europe/Moscow'
USE_I18N: bool = True
USE_L10N: bool = True
USE_TZ: bool = True

# endregion

# Static files (CSS, JavaScript, Images)
# region
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL: str = '/static/'
STATIC_ROOT: Path = BASE_DIR / 'staticfiles'
STATICFILES_DIRS: List[Path] = [
    BASE_DIR / 'static'
]
# endregion


# Github
# region
GITHUB_AUTH_TOKEN: str = env.str('GITHUB_AUTH_TOKEN', '')
GITHUB_WEBHOOK_TOKEN: str = env.str('GITHUB_WEBHOOK_TOKEN', '')
GITHUB_AUTH_CLIENT_ID: str = env.str('GITHUB_AUTH_CLIENT_ID', '')
GITHUB_AUTH_CLIENT_SECRET: str = env.str('GITHUB_AUTH_CLIENT_SECRET', '')
# endregion

# Google
# region
GTM_ID: str = env.str('GTM_ID', '')  # Google Tag Manager
# endregion

# Yandex
# region
YANDEX_VERIFICATION: bool = env.str('YANDEX_VERIFICATION', False)
# endregion

# Crispy
# region
CRISPY_TEMPLATE_PACK: str = 'bootstrap4'
# endregion

TEXT_COLUMNS: Tuple[str, ...] = ('name', 'organization', 'project', 'login')
