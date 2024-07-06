# its_portal/settings.py

from pathlib import Path
import environ
import os
from django.utils.translation import gettext_lazy as _

# Inicializar variables de entorno
env = environ.Env(
    DJANGO_SECRET_KEY=(str, ""),
    DJANGO_ENVIRONMENT=(str, "development"),
)

# Construir rutas dentro del proyecto como esta: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Tomar variables de entorno del archivo .env
environ.Env.read_env(env_file=str(BASE_DIR / ".env"))

# Configuración de inicio rápido para desarrollo - no apta para producción
# Ver https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# ADVERTENCIA DE SEGURIDAD: mantén la clave secreta usada en producción en secreto
SECRET_KEY = env("DJANGO_SECRET_KEY")

# Determinar si estamos en desarrollo o producción
ENVIRONMENT = env("DJANGO_ENVIRONMENT", "development")

# ADVERTENCIA DE SEGURIDAD: no ejecutes con debug activado en producción
DEBUG = ENVIRONMENT == "development"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "tudominio.com",
    "www.tudominio.com",
]

# Definición de la aplicación
INSTALLED_APPS = [
    "django.contrib.admin",  # Interfaz administrativa de Django
    "django.contrib.auth",  # Autenticación y autorización
    "django.contrib.contenttypes",  # Tipos de contenido
    "django.contrib.sessions",  # Gestión de sesiones
    "django.contrib.messages",  # Sistema de mensajes
    "django.contrib.staticfiles",  # Gestión de archivos estáticos
    "django.contrib.humanize",  # Plantillas humanizadoras (ej. formatear fechas y números)
    "django_extensions",  # Extensiones de Django para desarrolladores
    "django_ckeditor_5",  # Editor WYSIWYG CKEditor
    "main.apps.MainConfig",  # Aplicación principal
    "blog_app.apps.BlogConfig",  # Aplicación del blog
    "forum_app.apps.ForumAppConfig",  # Aplicación del foro
    "messages_app.apps.MessagesAppConfig",  # Aplicación de mensajes
    "projects_app.apps.ProjectsConfig",  # Aplicación de proyectos
]
# "client_portal.apps.ClientPortalConfig",  # Portal del cliente / eliminado
# "employee_portal.apps.EmployeePortalConfig",  # Portal del empleado / eliminado
# "its_admin.apps.ItsAdminConfig",  # Administración interna / eliminado

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "its_portal.middleware.AdminSessionMiddleware",
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

# Base de datos
# Ver https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Validación de contraseñas
# Ver https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Internacionalización
# Ver https://docs.djangoproject.com/en/3.2/topics/i18n/

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

# CKEDITOR_UPLOAD_PATH = "uploads/"
#
# CKEDITOR_5_CONFIGS = {
#    "default": {
#        "toolbar": [
#            "heading",
#            "|",
#            "bold",
#            "italic",
#            "underline",
#            "strikethrough",
#            "subscript",
#            "superscript",
#            "|",
#            "link",
#            "blockquote",
#            "code",
#            "codeBlock",
#            "|",
#            "numberedList",
#            "bulletedList",
#            "todoList",
#            "|",
#            "insertImage",
#            "|",
#            "textColor",
#            "bgColor",
#            "|",
#            "alignment",
#            "|",
#            "undo",
#            "redo",
#        ],
#        "image": {
#            "toolbar": ["imageTextAlternative", "imageStyle:full", "imageStyle:side"]
#        },
#        "table": {"contentToolbar": ["tableColumn", "tableRow", "mergeTableCells"]},
#        "extraPlugins": "image2,uploadimage",
#        "height": 400,
#        "width": "100%",
#    },
# }

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_5_CONFIGS = {
    "extends": {
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
        "height": 450,
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

# Configuración de almacenamiento de archivos estáticos con cache busting
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# Configuración de logging
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

# Configuraciones de seguridad para producción
if ENVIRONMENT == "production":
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = "DENY"
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    X_FRAME_OPTIONS = "SAMEORIGIN"
