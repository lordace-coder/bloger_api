import os
from datetime import timedelta
from pathlib import Path

from cloudinary import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-76=%fvyt_^#%jecb6ok$mdq7)084_xzjnty)syx^+qw-7bf*_3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*',

    ]

if DEBUG:
    ALLOWED_HOSTS.append('127.0.0.1')
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'posts',
    'notifications_and_messages',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'users',
    'cloudinary',
    'forgot_password',
    'staffpanel',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#CLOUDINARY_URL="cloudinary://524857684224764:GmlN577TzHP5YShkZFL2gBCw8V8@dinoc8svf"
config(
  cloud_name = "dinoc8svf",
  api_key = "524857684224764",
  api_secret = "GmlN577TzHP5YShkZFL2gBCw8V8",
  api_proxy = "http://proxy.server:3128"
)

import cloudinary.api
import cloudinary.uploader

# * FOR MEDIA
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ! REST FRAMEWORK SETTINGS
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [

        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication'
        # other authentication classes...
    ],
    # other settings...
}
CORS_ALLOWED_ORIGINS = [
    "https://blorger.netlify.app",
    "http://localhost:8000",
    "http://localhost:5173"
]
# CORS_ALLOW_ALL_ORIGINS= True
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME":timedelta(hours=5),
    "REFRESH_TOKEN_LIFETIME":timedelta(days=14),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "UPDATE_LAST_LOGIN":True,
    'TOKEN_SERIALIZER': 'users.custom_token_serializer.CustomTokenObtainPairSerializer',
    "USER_ID_FIELD":"username"
}




# ! FORGOT PASSWORD SETTINGS
FORGOT_PASSWORD_CONFIG = {
    'mail_template':"""
    Your Recovery Token is #token, please guard it wisely.
    """
}

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'bloggernetlify@gmail.com'
EMAIL_HOST_PASSWORD = 'ziihipjirjkojfvg'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_TIMEOUT = 50