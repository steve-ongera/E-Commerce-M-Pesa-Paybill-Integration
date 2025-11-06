
# Add to your settings.py

import os
from pathlib import Path
from decouple import config  # pip install python-decouple



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0l^x_1dp)fgb(w9+-)*grqfc4z(l$1w=^mwpd-pm_1&monmyiu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'paybill_ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'paybill_ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================
# M-PESA CONFIGURATION
# ============================================

# M-Pesa Environment (sandbox or production)
MPESA_ENVIRONMENT = config('MPESA_ENVIRONMENT', default='sandbox')

# M-Pesa Consumer Key and Secret (from Daraja Portal)
MPESA_CONSUMER_KEY = config('MPESA_CONSUMER_KEY', default='')
MPESA_CONSUMER_SECRET = config('MPESA_CONSUMER_SECRET', default='')

# M-Pesa Paybill/Business Shortcode
MPESA_SHORTCODE = config('MPESA_SHORTCODE', default='174379')  # Sandbox shortcode

# M-Pesa Passkey (from Daraja Portal)
MPESA_PASSKEY = config('MPESA_PASSKEY', default='')

# M-Pesa Callback URL (must be publicly accessible)
# Use ngrok for local testing: https://your-ngrok-url.ngrok.io/mpesa/callback/
MPESA_CALLBACK_URL = config(
    'MPESA_CALLBACK_URL', 
    default='https://yourdomain.com/mpesa/callback/'
)

# M-Pesa Timeout URLs (optional)
MPESA_TIMEOUT_URL = config(
    'MPESA_TIMEOUT_URL',
    default='https://yourdomain.com/mpesa/timeout/'
)

# ============================================
# CSRF SETTINGS FOR M-PESA CALLBACK
# ============================================
CSRF_TRUSTED_ORIGINS = [
    'https://sandbox.safaricom.co.ke',
    'https://api.safaricom.co.ke',
]

# Login URL
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/products/'
