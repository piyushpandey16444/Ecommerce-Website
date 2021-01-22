"""
Django settings for Ecommerce_Website project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR =os.path.join(BASE_DIR,'templates')
# TEMPLATE_DIR1 =os.path.join(BASE_DIR,'accounts/templates')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dyy7gt9u$8k4shebxv=8^ik1+uh2-5x68p*i6(*$(_nqk17p*m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]


# Application definition

INSTALLED_APPS = [
    'django_static_jquery3',
    'django_static_jquery_ui',
    'django_tabbed_changeform_admin',
    'admin_shortcuts',
    'vali',
    'easy_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'checkout.apps.CheckoutConfig',
    'paywix',
    'ckeditor',
    'ckeditor_uploader',
    'colorfield',
    'taggit',
    'crispy_forms',
    'hoitymoppet',
    'accounts',
    'generic_links',
    'enquiry_order',
    'mail_templated',
    'social_django',
    'djmoney',
    'django_countries',
    'rest_framework',
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.instagram.InstagramOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
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

ROOT_URLCONF = 'Ecommerce_Website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends', # add this
                'social_django.context_processors.login_redirect', # add this
            ],
        },
    },
]


VALI_CONFIG = {
        'theme': 'purple',
        'dashboard': {
            'name': 'Dashboard',
            'url': '/admin/dashboard/',
            # 'subtitle': 'Dashboard view with all statistics',
            'site_name': 'Hoitymoppet',
            'url_image_profile': ''
        },

        'fieldset': {
            'fields': ['user_permissions', 'permissions']
        },

        'applist': {
            'order': "registry", "group": True
        }
    }


WSGI_APPLICATION = 'Ecommerce_Website.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': 'Hoitymoppet',
        'NAME': 'Hoitymoppet_db',
        # 'HOST':'127.0.0.1',
        # 'PORT': '8000',
        # 'USERNAME':'root',
        # 'PASSWORD':'root',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# Adding and creating media folder for storing images
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# code for payu merchant details
PAYU_CONFIG = {
    "merchant_key": "zsbmgrsB",
    "merchant_salt": "61tGsmxuBr",
    # "authorization": "SL5/I9CqRdiAoRwN4mv1zDhnGt1hBAnjISpVdoB9Vfc=",
    "mode": "test",
    "success_url": "http://127.0.0.1:8000/checkout/checkout/success/",
    "failure_url": "http://127.0.0.1:8000/checkout/checkout/failure/"
}
# End


# Adding bootstrap4 templates for signup form
CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'index'

LOGIN_URL = 'login'
# LOGIN_REDIRECT_URL = 'home'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'login'

#################################################################################################################################################################
SITE_ID = 1
####################################
##  CKEDITOR CONFIGURATION ##
####################################
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js'

CKEDITOR_UPLOAD_PATH = '/media/'
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}
#################################################################################################################################################################

# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'devashishmishra786@gmail.com'
# EMAIL_HOST_PASSWORD = 'devathegreat'
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'TestSite Team <noreply@example.com>'

#
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_USER = 'assistwebtech@gmail.com'
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
EMAIL_HOST_PASSWORD = 'dreamweaver2012'


# Social Accounts Access

# SOCIAL_AUTH_LOGIN_ERROR_URL = '/settings/'
# SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/settings/'
# SOCIAL_AUTH_RAISE_EXCEPTIONS = False

SOCIAL_AUTH_FACEBOOK_KEY = '186887785908778'        # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'bb46f83f7518186141e5935f610886da' # App Secret
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_link']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email, picture.type(large), link'
}
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [
    ('name', 'name'),
    ('email', 'email'),
    ('picture', 'picture'),
    ('link', 'profile_url'),
]


SOCIAL_AUTH_INSTAGRAM_KEY = '197569278265080'
SOCIAL_AUTH_INSTAGRAM_SECRET = 'db62f827757dc1c736881a728118b51e'
SOCIAL_AUTH_INSTAGRAM_EXTRA_DATA = [
    ('user', 'user'),
]


SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = 'xxxxxxxxxxxxxxxxxxxx'
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = 'xxxxxxxxxxxxxxxxxxxx'
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_basicprofile', 'r_emailaddress']
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['email-address', 'formatted-name', 'public-profile-url', 'picture-url']
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [
    ('id', 'id'),
    ('formattedName', 'name'),
    ('emailAddress', 'email_address'),
    ('pictureUrl', 'picture_url'),
    ('publicProfileUrl', 'profile_url'),
]





ADMIN_SHORTCUTS = [
    # {
    #     'shortcuts': [
    #         {
    #             'url': '/',
    #             'title': 'Home',
    #             'open_new_window': True,
    #         },
    #         {
    #             'title': 'Users',
    #             'url_name': 'admin:auth_user_changelist',
    #             # 'count': 'example.utils.count_users',
    #         },
    #         {
    #             'title': 'Groups',
    #             'url_name': 'admin:auth_group_changelist',
    #             # 'count': 'example.utils.count_groups',
    #         },
    #         {
    #             'title': 'Add user',
    #             'url_name': 'admin:auth_user_add',
    #             # 'has_perms': 'example.utils.has_perms_to_users',
    #         },
    #     ]
    # },
    {
        # 'title': 'CMS',
        'shortcuts': [
            {
                'title': 'Total Users',
                'url_name': 'admin:auth_user_changelist',
                'count_new': 'Ecommerce_Website.utils.count_users',
            },
            {
                'title': 'Products',
                'url_name': 'admin:hoitymoppet_product_changelist',
                'count_new': 'Ecommerce_Website.utils.count_products',
            },
            {
                'title': 'Total Orders',
                'url_name': 'admin:enquiry_order_order_changelist',
                'count_new': 'Ecommerce_Website.utils.count_orders',
            },
            {
                'title': 'Orders (Confirm)',
                'url': '/admin/enquiry_order/order/?status_name__exact=Confirm',
                'count_new': 'Ecommerce_Website.utils.count_orders_confirm',
            },
            {
                'title': 'Orders (Dispatch)',
                'url': '/admin/enquiry_order/order/?status_name__exact=Dispatch',
                'count_new': 'Ecommerce_Website.utils.count_orders_dispatch',
            },
            {
                'title': 'Orders (Shiped)',
                'url': '/admin/enquiry_order/order/?status_name__exact=Shiped',
                'count_new': 'Ecommerce_Website.utils.count_orders_shiped',
            },
            {
                'title': 'Orders (Delivered)',
                'url': '/admin/enquiry_order/order/?status_name__exact=Delivered',
                'count_new': 'Ecommerce_Website.utils.count_orders_delivered',
            },
            {
                'title': 'Categories',
                'url_name': 'admin:generic_links_categories_changelist',
                'count_new': 'Ecommerce_Website.utils.count_categories',
            },
            {
                'title': 'Enquiry',
                'url_name': 'admin:enquiry_order_userqueries_changelist',
                'count_new': 'Ecommerce_Website.utils.count_enquiries',
            },
        ]
    },
]
ADMIN_SHORTCUTS_SETTINGS = {
    'show_on_all_pages': True,
    'hide_app_list': True,
    'open_new_window': False,
}