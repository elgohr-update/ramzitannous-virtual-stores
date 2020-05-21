"""
Django settings for api project.

Generated by "django-admin startproject" using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import pathlib
from datetime import timedelta

import dj_database_url

from settings.log import *
from shared.utils import get_env
from settings.rest_framework import *
import dotenv

dotenv.load_dotenv()

BASE_DIR = pathlib.Path(os.path.dirname(__file__)).parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "xv+-#_8yxr^jb4$wqvl)&ugy#=i0f%pnj6%a)(s!fc9)w7-z6s"

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MY_APPS = [
    "shared",
    "accounts.apps.AccountsConfig",
    "stores",
    "products.apps.ProductsConfig"
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_celery_beat",
    "drf_yasg",
    "django_filters",
    "djoser",
    "versatileimagefield"
]

INSTALLED_APPS += MY_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "shared.middlewares.HeaderMiddleware"
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = REST_FRAMEWORK

AUTH_USER_MODEL = "accounts.Account"

DATA_UPLOAD_MAX_MEMORY_SIZE = 500 * 1000 * 1000  # Max 500 MBs

LOGGING = LOGGING

LOGIN_URL = "/auth/login"

LOGOUT_URL = "/auth/logout"

enable_email = bool(int(get_env("ENABLE_EMAIL")))

DJOSER = {
    "SERIALIZERS": {
        "user": "accounts.serializers.AccountGetSerializer",
        "current_user": "accounts.serializers.AccountGetSerializer",
        "user_create_password_retype": "accounts.serializers.AccountCreateSerializer",
    },
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "USER_CREATE_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_URL": "#/password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "#/username/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "#/activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": enable_email,
    "SEND_CONFIRMATION_EMAIL": enable_email,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": enable_email,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": enable_email,
    "TOKEN_MODEL": None
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
}

SWAGGER_SETTINGS = {
    "DEFAULT_AUTO_SCHEMA_CLASS": "shared.schema.StoreSchema",
    "TAGS_SORTER": "alpha"
}

# celery
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_TASK_IGNORE_RESULT = False
CELERY_TASK_ALWAYS_EAGER = False

CELERY_BROKER_URL = get_env("REDIS_URL")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

# requests
REQUEST_DEFAULT_TIMEOUT = 60
REQUEST_DEFAULT_BACKOFF = 0.5
REQUEST_DEFAULT_RETRIES = 3

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = "static"

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR.parent / "media"

# email
if enable_email:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = get_env("EMAIL_HOST")
    EMAIL_PORT = int(get_env("EMAIL_PORT"))
    EMAIL_HOST_USER = get_env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = get_env("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = get_env("DEFAULT_FROM_EMAIL")
else:
    EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"

DATABASES = {
    "default": dj_database_url.config(default=get_env("DATABASE_URL"), conn_max_age=600)
}


VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    "profile": [
        ("full_size", "url"),
        ("thumbnail", "thumbnail__500x500"),
    ],
    "product": [
        ("product_large", "thumbnail__1080x1080"),
        ("product_small", "thumbnail__120x120"),
        ("product_meduim", "thumbnail__510x510"),
    ],
    "category": [
        ("thumbnail", "thumbnail__250x250"),
    ],
    "store": [
        ("thumbnail", "thumbnail__960x960"),
    ]
}

VERSATILEIMAGEFIELD_SETTINGS = {
    "create_images_on_demand": False
}
