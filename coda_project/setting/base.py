import os
from pickle import TRUE

import django_heroku
import redis

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ["*"]
# ALLOWED_HOSTS = ['127.0.0.1','localhost','codatrainingapp.herokuapp.com','www.codanalytics.net','codanalytics.net']
# ALLOWED_HOSTS = []
AUTH_USER_MODEL = "accounts.CustomerUser"
AUTHENTICATION_BACKENDS = (("django.contrib.auth.backends.ModelBackend"),)


# Application definition
INSTALLED_APPS = [
    "main.apps.MainConfig",
    #'users.apps.UsersConfig',
    "accounts.apps.AccountsConfig",
    "codablog.apps.CodablogConfig",
    "data.apps.DataConfig",
    "application.apps.ApplicationConfig",
    "getdata.apps.GetdataConfig",
    "projectmanagement.apps.ProjectmanagementConfig",
    "investing.apps.InvestingConfig",
    "management.apps.ManagementConfig",
    "globalsearch.apps.GlobalsearchConfig",
    "finance.apps.FinanceConfig",
    "store",
    "crispy_forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",
    "django_countries",
    "mathfilters",
    "mptt",
    "django_filters",
    "django_celery_beat",
    "django_celery_results",
    #'dbbackup',
    # "django_extensions",
    # "django_crontab",
    # 'testing.apps.TestingConfig',
]
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


CRONJOBS = [
    # ("*/1 * * * *", "coda_project.cron.my_backup"),
    ("*/5 * * * *", "management.cron.advertisement"),
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

CSRF_COOKIE_SECURE = False

ROOT_URLCONF = "coda_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # os.path.join(BASE_DIR, 'templates')
            "templates"
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "management.context_processors.categories",
                "management.context_processors.departments",
            ],
        },
    },
]

WSGI_APPLICATION = "coda_project.wsgi.application"

CELERY_BROKER_URL = "redis://default:X7riK5cCiJMQa0qpZr23qzAizQpzjvSz@redis-19459.c52.us-east-1-4.ec2.cloud.redislabs.com:19459"
CELERY_RESULT_BACKEND = "redis://default:X7riK5cCiJMQa0qpZr23qzAizQpzjvSz@redis-19459.c52.us-east-1-4.ec2.cloud.redislabs.com:19459"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_IMPORTS = "coda_project.task"

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    "run_on_every_1st": {
        "task": "task_history",
        "schedule": crontab(0, 0, day_of_month="1"),
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_URL = "/static/"
STATICFILES_DIR = os.path.join(BASE_DIR, "static")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

CRISPY_TEMPLATE_PACK = "bootstrap4"

LOGIN_REDIRECT_URL = "main:layout"
LOGIN_URL = "accounts:account-login"

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR + "/emails"

AWS_S3_REGION_NAME = "us-east-2"  # change to your region
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

django_heroku.settings(locals())

CELERY_BROKER_URL = "redis://default:xjaoROhpU8Lbiz8OZskVTgyYDFAdSmlo@redis-11854.c240.us-east-1-3.ec2.cloud.redislabs.com:11854"
CELERY_RESULT_BACKEND = "redis://default:xjaoROhpU8Lbiz8OZskVTgyYDFAdSmlo@redis-11854.c240.us-east-1-3.ec2.cloud.redislabs.com:11854"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_IMPORTS = "coda_project.task"

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    "run_on_every_1st": {
        "task": "task_history",
        "schedule": crontab(0, 0, day_of_month="1"),
        #'schedule': crontab(),
    },
}

