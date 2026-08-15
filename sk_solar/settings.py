"""
Django settings for sk_solar project.
"""

import os
from pathlib import Path



import dj_database_url
from django.contrib.gis import db
from django.template.backends import django


BASE_DIR = Path(__file__).resolve().parent.parent


if os.name == "nt":
    default_sqlite_path = Path(
        os.environ.get(
            "SQLITE_PATH",
            Path.home() / "AppData" / "Local" / "sk_solar" / "db.sqlite3",
        )
    )
else:
    default_sqlite_path = BASE_DIR / "db.sqlite3"
default_sqlite_path.parent.mkdir(parents=True, exist_ok=True)


SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-_t0ovgfnysyb^p1#xsha#-mg6r49q*^c-bu!7mwj-w@a7er(-x",
)
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

default_allowed_hosts = "127.0.0.1,localhost,0.0.0.0,testserver"
allowed_hosts = os.environ.get("ALLOWED_HOSTS", default_allowed_hosts)
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts.split(",") if host.strip()]
ALLOWED_HOSTS.extend([".onrender.com"])

if DEBUG and "*" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("*")


INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "website",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sk_solar.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sk_solar.wsgi.application"


DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_CONN_MAX_AGE = int(os.environ.get("DATABASE_CONN_MAX_AGE", "600"))
DATABASE_SSL_REQUIRE = os.environ.get("DATABASE_SSL_REQUIRE", str(not DEBUG)).lower() == "true"
database_default_url = DATABASE_URL or f"sqlite:///{default_sqlite_path}"
database_is_sqlite = database_default_url.startswith("sqlite")


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD':'Aditya@123',
        'HOST': 'localhost',
        'PORT': '5432',
    },

    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_recovery.sqlite3',
    }
}
    




AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if not DEBUG:
    CSRF_TRUSTED_ORIGINS = [
        origin.strip()
        for origin in os.environ.get(
            "CSRF_TRUSTED_ORIGINS",
            "https://*.onrender.com",
        ).split(",")
        if origin.strip()
    ]
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
