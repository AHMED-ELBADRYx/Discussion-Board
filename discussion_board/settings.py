"""
Django settings for discussion_board project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# # Security Settings
# SECRET_KEY = 'django-insecure-y1*p(c@690hw@de=*e01^@1%d#0wh8s8)z15kib078!r2jdduq'
# DEBUG = True
# ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # For better date/number formatting
    
    # Local apps
    'boards.apps.BoardsConfig',
    'accounts.apps.AccountsConfig',
    
    # Third party apps
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'accounts.middleware.CustomCSRFMiddleware',
     'django.middleware.csrf.CsrfViewMiddleware', 
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'discussion_board.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'discussion_board.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# # Static files finders
# STATICFILES_FINDERS = [
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# ]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication Settings
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

# # Session and CSRF Settings
# SESSION_SAVE_EVERY_REQUEST = True
# SESSION_COOKIE_AGE = 86400  # 24 hours
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# CSRF_USE_SESSIONS = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# # Security settings for production (disabled in DEBUG mode)
# if DEBUG:
#     SESSION_COOKIE_SECURE = False
#     CSRF_COOKIE_SECURE = False
#     SECURE_SSL_REDIRECT = False
# else:
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     SECURE_SSL_REDIRECT = True
#     SECURE_HSTS_SECONDS = 31536000
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#     SECURE_HSTS_PRELOAD = True
#     SECURE_CONTENT_TYPE_NOSNIFF = True
#     SECURE_BROWSER_XSS_FILTER = True
#     X_FRAME_OPTIONS = 'DENY'

# Messages Framework
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# # Email Configuration (for development)
# if DEBUG:
#     EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# else:
#     EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#     EMAIL_HOST = 'smtp.gmail.com'
#     EMAIL_PORT = 587
#     EMAIL_USE_TLS = True
#     EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
#     EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Default "from" email
DEFAULT_FROM_EMAIL = 'noreply@discussionboard.com'
SERVER_EMAIL = 'admin@discussionboard.com'

# Email Configuration (for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache Configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'discussion-board-cache',
    }
}

# # Cache timeout settings
# CACHE_MIDDLEWARE_ALIAS = 'default'
# CACHE_MIDDLEWARE_SECONDS = 600
# CACHE_MIDDLEWARE_KEY_PREFIX = ''

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'accounts': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'boards': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# # Ensure logs directory exists
# LOG_DIR = BASE_DIR / 'logs'
# LOG_DIR.mkdir(exist_ok=True)

# Pagination settings
PAGINATE_BY = 20
TOPICS_PER_PAGE = 20
POSTS_PER_PAGE = 15

# # File upload settings
# FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
# DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# # User session settings
# SESSION_COOKIE_NAME = 'discussionboard_sessionid'
# SESSION_COOKIE_HTTPONLY = True
# SESSION_COOKIE_SAMESITE = 'Lax'

# # CSRF settings
# CSRF_COOKIE_NAME = 'discussionboard_csrftoken'
# CSRF_COOKIE_HTTPONLY = True
# CSRF_COOKIE_SAMESITE = 'Lax'
# CSRF_TRUSTED_ORIGINS = []

# # Custom user model (if you want to extend it later)
# # AUTH_USER_MODEL = 'accounts.User'

# # Time zone choices for user profiles
# TIME_ZONE_CHOICES = [
#     ('UTC', 'UTC'),
#     ('US/Eastern', 'US Eastern'),
#     ('US/Central', 'US Central'),
#     ('US/Mountain', 'US Mountain'),
#     ('US/Pacific', 'US Pacific'),
#     ('Europe/London', 'Europe London'),
#     ('Europe/Paris', 'Europe Paris'),
#     ('Asia/Tokyo', 'Asia Tokyo'),
# ]

# Application specific settings
DISCUSSION_BOARD_SETTINGS = {
    'ALLOW_GUEST_VIEWING': True,
    'REQUIRE_EMAIL_VERIFICATION': False,
    'ALLOW_USER_REGISTRATION': True,
    'MAX_TOPICS_PER_BOARD': 1000,
    'MAX_POSTS_PER_TOPIC': 500,
    'ENABLE_MODERATION': False,
}

# # Development settings
# if DEBUG:
#     # Django Debug Toolbar (if installed)
#     try:
#         import debug_toolbar
#         INSTALLED_APPS += ['debug_toolbar']
#         MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
#         INTERNAL_IPS = ['127.0.0.1', 'localhost']
        
#         DEBUG_TOOLBAR_CONFIG = {
#             'DISABLE_PANELS': [
#                 'debug_toolbar.panels.redirects.RedirectsPanel',
#             ],
#             'SHOW_TEMPLATE_CONTEXT': True,
#         }
#     except ImportError:
#         pass
    
#     # Allow all origins in development
#     ALLOWED_HOSTS = ['*']
    
#     # Disable caching in development
#     CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'

# # Production settings override
# if not DEBUG:
#     # Security settings
#     SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#     USE_TZ = True
    
#     # Database connection pooling (if using PostgreSQL)
#     # DATABASES['default']['CONN_MAX_AGE'] = 60
    
#     # Static files compression
#     STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    
#     # Admin settings
#     ADMINS = [
#         ('Admin', 'admin@discussionboard.com'),
#     ]
#     MANAGERS = ADMINS

# Environment-specific settings
try:
    from .local_settings import *
except ImportError:
    pass

# # Load environment variables
# if os.path.exists(BASE_DIR / '.env'):
#     from dotenv import load_dotenv
#     load_dotenv(BASE_DIR / '.env')
    
# DEBUG = os.environ.get('DEBUG', 'True') == 'True'
# SECRET_KEY = os.environ.get('SECRET_KEY', 'default-key-here')