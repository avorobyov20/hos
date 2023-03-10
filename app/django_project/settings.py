# Generated by 'django-admin startproject' command
# https://docs.djangoproject.com/en/4.1/ref/settings/

from os import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = environ.get("SECRET_KEY")
DEBUG = int(environ.get("DEBUG", default=0))
ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS").split(" ")

ROOT_URLCONF = "django_project.urls"
WSGI_APPLICATION = "django_project.wsgi.application"

AUTH_USER_MODEL = "main.AdvUser"
PUBLIC_GROUP_ID = 1
AAC_URL_PREFIX = environ.get("AAC_URL_PREFIX")

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DATABASES = {
    "default": {
        "ENGINE": environ.get("POSTGRES_ENGINE", "django.db.backends.sqlite3"),
        "NAME": environ.get("POSTGRES_DB", BASE_DIR / "db.sqlite3"),
        "USER": environ.get("POSTGRES_USER", "user"),
        "PASSWORD": environ.get("POSTGRES_PASSWORD", "password"),
        "HOST": environ.get("POSTGRES_HOST", "localhost"),
        "PORT": environ.get("POSTGRES_PORT", "5432"),
    }
}

INSTALLED_APPS = [
    "main.admin_config.MainAdminConfig",
    #  "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main.apps.MainConfig",
    "bootstrap4",
    "django_cleanup",
    "easy_thumbnails",
    "adminsortable2",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "main" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "main.middlewares.hos_context_processor",
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        + "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        + "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        + "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        + "NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.mail.ru"
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = environ.get("EMAIL_HOST_USER")

THUMBNAIL_BASEDIR = "thumbnails"
THUMBNAIL_ALIASES = {
    "main.Genre": {
        "default": {
            "size": (200, 0),
            "crop": "scale",
        },
    },
    "main.Pgm": {
        "default": {
            "size": (200, 0),
            "crop": "scale",
        },
    },
    "main.Track": {
        "default": {
            "size": (80, 80),
            "crop": "scale",
        },
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'warning.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

if environ.get("CSRF_TRUSTED_ORIGINS"):
    CSRF_TRUSTED_ORIGINS = environ.get("CSRF_TRUSTED_ORIGINS").split(" ")
else:
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:1337",
    ]

SERVICE_NAME = "HOS Admin"
HOST_NAME = "Slow music for fast times"
