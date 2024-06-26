from pathlib import Path
from common.utils.env import get_env_vars


BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_ENV_VARS = get_env_vars(
    "DATABASE_NAME",
    "DATABASE_USER",
    "DATABASE_PASSWORD",
    "DATABASE_HOST",
    # "DATABASE_PORT",
)

SECRET_KEY = "django-insecure-)u+cvkifeigjb*t_19&1(vk#py-ypsa6=t$it1z4a=6z^k%oqa"

DEBUG = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "host.docker.internal",
    "127.0.0.1",
    ".vercel.app",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "djoser",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "list",
    "list_item",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "simplgrocr_backend.urls"

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

WSGI_APPLICATION = "simplgrocr_backend.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DATABASE_ENV_VARS["DATABASE_NAME"],
        "USER": DATABASE_ENV_VARS["DATABASE_USER"],
        "PASSWORD": DATABASE_ENV_VARS["DATABASE_PASSWORD"],
        "HOST": DATABASE_ENV_VARS["DATABASE_HOST"],
        # "PORT": DATABASE_ENV_VARS["DATABASE_PORT"],
    },
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "SimplGrocr API",
    "DESCRIPTION": "SimplGrocr API",
    "VERSION": "1.0.0",
}


CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://host.docker.internal:3000"]

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

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
