import os
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = []
INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'daphne',

    'django.contrib.staticfiles',
    'django.contrib.sites',

    # 3rd party
    'rest_framework',

    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',

    "debug_toolbar",
    'social_django',
    'django_celery_beat',
    'django_filters',
    'drf_spectacular',

    'channels',

    # apps
    'users',
    'vacancies',
    'bands',
    'news',
    'notifications',
    'chat',

]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",

]

AUTH_USER_MODEL = 'users.User'

# OAuth2

AUTHENTICATION_BACKENDS = (

    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.github.GithubOAuth2',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIAL_AUTH_JSONFIELD_ENABLED = True

SOCIAL_AUTH_GITHUB_KEY = os.getenv('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.getenv('SOCIAL_AUTH_GITHUB_SECRET')

# dj-rest-auth

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'jwt-auth',
}

SITE_ID = 1

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Channels
ASGI_APPLICATION = 'config.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.getenv('REDIS_HOST'), 6379)],
        }
    }
}

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Cache

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{os.getenv('REDIS_HOST')}:6379",
        "OPTIONS": {
            "db": "0",
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

SESSION_COOKIE_AGE = 1209600
SESSION_SAVE_EVERY_REQUEST = False

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators


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

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# drf-spectacular Settings

SPECTACULAR_SETTINGS = {
    'TITLE': 'FindYourBand API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file-formatter': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'level': 'INFO',

        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'file-formatter',
            'level': 'DEBUG',
            'filename': BASE_DIR / 'logs' / 'django-logs.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 mb
            'backupCount': 5,

        }
    },

    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },

    'loggers': {
        'vacancies': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },

    },
}

# Email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

EMAIL_SERVER = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

# Celery

CELERY_BROKER_URL = f'redis://{os.getenv("REDIS_HOST")}:6379/1'
CELERY_RESULT_BACKEND = f'redis://{os.getenv("REDIS_HOST")}:6379/1'

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Celery Beat

CELERY_BEAT_SCHEDULE = {
    'send_daily_email_if_user_inactive_for_year': {
        'task': 'users.tasks.send_daily_email_if_user_inactive_for_year',
        'schedule': crontab(minute=0, hour=0),
    },
    'delete_account_if_user_inactive_long_time': {
        'task': 'users.tasks.delete_account_if_user_inactive_long_time',
        'schedule': crontab(minute=0, hour=0),
    },
}


# Django Debug Toolbar Docker Settings

def show_toolbar_callback(*args, **kwargs):
    if os.getenv("LOCAL_DEV"):
        return True
    return False


DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_toolbar_callback,
                        'IS_RUNNING_TESTS': False}
