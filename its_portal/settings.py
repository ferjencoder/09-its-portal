# its_portal/settings.py

from pathlib import Path
import environ
import os
from django.utils.translation import gettext_lazy as _

# Initialize environment variables
env = environ.Env(
    DJANGO_SECRET_KEY=(str, ""),
    DJANGO_ENVIRONMENT=(str, "development"),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(env_file=str(BASE_DIR / ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# Determine if we are in development or production
ENVIRONMENT = env("DJANGO_ENVIRONMENT", "development")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENVIRONMENT == "development"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "yourdomain.com",
    "www.yourdomain.com",
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django_extensions",
    "django_ckeditor_5",
    # "ckeditor_uploader",
    "main",
    "blog",
    "client_portal",
    "employee_portal",
    "forum_app",
    "its_admin",
    "messages_app",
    "projects",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "its_portal.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates"), BASE_DIR / "templates"],
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

WSGI_APPLICATION = "its_portal.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", _("English")),
    ("es", _("Spanish")),
]

TIME_ZONE = "UTC"

USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [BASE_DIR / "its_portal/static"]

SESSION_COOKIE_NAME = "sessionid_frontend"
CSRF_COOKIE_NAME = "csrftoken_frontend"

ADMIN_SESSION_COOKIE_NAME = "sessionid_admin"
ADMIN_CSRF_COOKIE_NAME = "csrftoken_admin"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "underline",
            "strikethrough",
            "subscript",
            "superscript",
            "|",
            "link",
            "blockquote",
            "code",
            "codeBlock",
            "|",
            "numberedList",
            "bulletedList",
            "todoList",
            "|",
            "insertImage",
            "mediaEmbed",
            "insertTable",
            "|",
            "textColor",
            "bgColor",
            "|",
            "alignment",
            "|",
            "undo",
            "redo",
        ],
        "image": {
            "toolbar": ["imageTextAlternative", "imageStyle:full", "imageStyle:side"]
        },
        "table": {"contentToolbar": ["tableColumn", "tableRow", "mergeTableCells"]},
        "extraPlugins": "image2,uploadimage",
        "height": 400,
        "width": "100%",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "https://127.0.0.1:8000",
]

CSRF_COOKIE_SECURE = False
CSRF_FAILURE_VIEW = "main.views.csrf_failure"

LOGIN_URL = "main:login"
LOGIN_REDIRECT_URL = "main:profile"
LOGOUT_REDIRECT_URL = "main:home"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": True,
        },
        "main": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}

# Security settings for production
if ENVIRONMENT == "production":
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    X_FRAME_OPTIONS = "SAMEORIGIN"
