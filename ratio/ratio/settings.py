"""Create your own .env by following
the sample.env example"""

import os

import environ
from django.utils.translation import ugettext_lazy as _

root = environ.Path(__file__) - 3

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)

environ.Env.read_env(root('.env'))

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = env.bool('DEBUG')

DEFAULT_CHARSET = 'utf-8'

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

EMAIL_HOST = env('EMAIL_HOST')

EMAIL_HOST_USER = env('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

EMAIL_PORT = env('EMAIL_PORT')

EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')

EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL')

ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE = True

ENABLE_USER_ACTIVATION = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DISABLE_USERNAME = False

INSTALLED_APPS = [
    'bootstrap4',
    'competition',
    'cookielaw',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hreflang',
    'school',
    'tinymce'
]

LANGUAGE_CODE = env.str("LANGUAGE_CODE")

LANGUAGES = (
    ('en', _('English')),
    ('it', _('Italian')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LOGIN_VIA_EMAIL = True

LOGIN_VIA_EMAIL_OR_USERNAME = True

LOGIN_REDIRECT_URL = 'school:index'

LOGIN_URL = 'school:log_in'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME = False

ROOT_URLCONF = 'ratio.urls'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

SITE_ID = 1

SIGN_UP_FIELDS = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

STATIC_ROOT = env.str('STATIC_ROOT')

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'ratio/static')
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_REMEMBER_ME = True

USE_TZ = True

WSGI_APPLICATION = 'ratio.wsgi.application'
