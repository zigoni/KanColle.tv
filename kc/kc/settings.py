"""
Django settings for kc project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('KC_SECRET_KEY', 'o60^c*mj-2ukntm$7=vf20v(9t41ea-#xw3j=$&b8+1s&yov3i')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('KC_DEBUG', False))

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kc_base',
    'kc_user',
    'kc_doujin',
    'kc_donate',
    'kc_home',
    'crispy_forms',
    'sendfile',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'kc.urls'

WSGI_APPLICATION = 'kc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = os.environ.get('KC_LANGUAGE_CODE', 'zh-cn')

TIME_ZONE = os.environ.get('KC_TIME_ZONE', 'Asia/Shanghai')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Custom user model
AUTH_USER_MODEL = 'kc_user.KcUser'

# Email
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = os.environ.get('KC_EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('KC_EMAIL_PORT', 465))
EMAIL_HOST_USER = os.environ.get('KC_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('KC_EMAIL_HOST_PASSWORD')

# Login
LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/user/'

# sendfile
SENDFILE_BACKEND = os.environ.get('KC_SENDFILE_BACKEND', 'sendfile.backends.simple')
SENDFILE_ROOT = os.path.join(BASE_DIR, '_rar')
SENDFILE_URL = '/rar'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}