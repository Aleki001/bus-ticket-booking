from pathlib import Path
import os
import environ

env = environ.Env()
environ.Env.read_env()




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-wmq6kb2u5ijou$n49o5f(f9(@qbxm+5p*dpp$5rn)g@g6ht9j0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'busapp',
    'user',

    'crispy_forms',
    'crispy_bootstrap4',
    'django_daraja',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'busbooking.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug' : True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'busbooking.wsgi.application'

# DATABASE CONFIGURATIONS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bus_ticket_booking',
        'USER': 'root',
        'PASSWORD': 'Wababe8843',
        'HOST': 'localhost', 
        'PORT': '3306',  
    }
}


# Password validation
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_TEMPLATE_PACK = 'bootstrap4'  # or 'bootstrap5', 'bootstrap3', depending on your version


# Mpesa configuration
MPESA_ENVIRONMENT = env('MPESA_ENVIRONMENT')
MPESA_CONSUMER_KEY = env('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = env('MPESA_CONSUMER_SECRET')
MPESA_SHORT_CODE = env('MPESA_SHORT_CODE')
MPESA_EXPRESS_SHORTCODE = env('MPESA_EXPRESS_SHORTCODE')
MPESA_INITIATOR_NAME = env('MPESA_INITIATOR_NAME')
MPESA_INITIATOR_PASSWORD = env('MPESA_INITIATOR_PASSWORD')
MPESA_RESULT_URL = env('MPESA_RESULT_URL')
MPESA_QUEUE_TIMEOUT_URL = env('MPESA_QUEUE_TIMEOUT_URL')
MPESA_CALLBACK_URL = env('MPESA_CALLBACK_URL')
MPESA_PASSKEY = env('MPESA_PASSKEY')
MPESA_ACCOUNT_BALANCE_TIMEOUT = env('MPESA_ACCOUNT_BALANCE_TIMEOUT')
MPESA_ACCOUNT_BALANCE_RESULT = env('MPESA_ACCOUNT_BALANCE_RESULT')



# SOCIAL LOGINS 

SITE_ID = 1


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email'
        ],
        'APP': {
            'client_id': env('GOOGLE_CLIENT_ID'),
            'secret': env('GOOGLE_SECRET'),
        },
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }   
}


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

# settings for celery
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"


# Email configurations
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
