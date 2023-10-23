"""
Django settings for Progressao project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os


# Adicione o ASGI_APPLICATION
ASGI_APPLICATION = "Progressao.asgi.application"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!ph7usvbsvm2k#f@%!%v=$ggv*s-f=&1(@rakrh+czsv*$6c9*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# settings.py

# settings.py

#ALLOWED_HOSTS = ['contextus.ibict.br', '172.16.17.41']
ALLOWED_HOSTS =['*']
#CSRF_TRUSTED_ORIGINS = ['http://contextus.ibict.br']
#CSRF_TRUSTED_ORIGINS = ['*']


# Application definition

INSTALLED_APPS = [

    # 'usuarios',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'paginas.apps.PaginasConfig',

    # 'nomedoapp.apps.NomedoappConfig'
]
AUTH_USER_MODEL = 'paginas.CustomUser'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'



CORS_ORIGIN_ALLOW_ALL = True
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'Progressao.middleware.StaffOnlyMiddleware',
    
]
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
ROOT_URLCONF = 'Progressao.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'paginas', 'templates'),
        ],
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

WSGI_APPLICATION = 'Progressao.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'testy',
        'USER': 'postgres',
        'PASSWORD': 'SENHA',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'testy',
        'USER': 'postgres',
        'PASSWORD': 'SENHA',
        'HOST': 'localhost',
        'PORT': '5432',
    },
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

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

# USE_L10N = True #modifiquei

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# STATIC_URL = 'static/'

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),  # comentei agr
# Importe a biblioteca os no início do arquivo

# ...

# Configurações estáticas
STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Configurações de banco de dados
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração de autenticação
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Configuração de redirecionamento após login e logout
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

# Configurações de email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Replace with your SMTP server address
EMAIL_PORT = 587  # Replace with your SMTP server port
EMAIL_USE_TLS = True  # Use TLS for secure communication
EMAIL_HOST_USER = 'milenafaria1706@gmail.com'
EMAIL_HOST_PASSWORD = 'ckwktyijrxlltfjo'
