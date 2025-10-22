"""
Django settings for Q360 Evaluation System.

This is a production-ready settings file for a 360-degree evaluation system
designed for government sector organizations.
"""

import os
from pathlib import Path
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def env_bool(name: str, default: bool = False) -> bool:
    """
    Convert environment variable values to booleans.

    Recognises typical truthy strings so non-standard casing (e.g. "TRUE")
    continues to work when toggling deployment flags.
    """
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {'true', '1', 'yes', 'on'}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-in-production')
DATA_ENCRYPTION_KEY = os.getenv('DATA_ENCRYPTION_KEY')
DEBUG = env_bool('DEBUG', True)  # Development mode
ALLOWED_HOSTS = ['*']  # Allow all hosts in development

# Application definition
INSTALLED_APPS = [
    'jazzmin',  # Modern admin interface
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',  # PostgreSQL full-text search

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'simple_history',
    'mptt',  # Django MPTT for hierarchical data
    # 'channels',  # Real-time notifications (commented out - install channels if needed)
    # 'csp',  # Content Security Policy (commented out - install django-csp if needed)
    # 'django_ratelimit',  # Rate limiting (commented out - install django-ratelimit if needed)

    # Local apps
    'apps.accounts',
    'apps.departments',
    'apps.evaluations',
    'apps.notifications',
    'apps.reports',
    'apps.development_plans',
    'apps.audit',
    'apps.sentiment_analysis',
    'apps.support',
    'apps.competencies',
    'apps.training',
    'apps.search',
    'apps.workforce_planning',
    'apps.continuous_feedback',
    'apps.compensation',
    'apps.leave_attendance',
    'apps.recruitment',
    'apps.dashboard',
    'apps.onboarding',
    'apps.wellness',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files (commented out)
    # 'csp.middleware.CSPMiddleware',  # Content Security Policy (commented out)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # i18n support
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'templates' / 'base',  # expose shared base layout as root-level template
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',  # i18n support
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# Use SQLite for development (switch to PostgreSQL for production)
# SQLite Configuration (for development/testing only)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#         'OPTIONS': {
#             'timeout': 20,  # Increase timeout to 20 seconds to avoid database locked errors
#         },
#     }
# }

# PostgreSQL Configuration (ACTIVE)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'q360_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'az'  # Default language: Azerbaijani

LANGUAGES = [
    ('az', _('Azərbaycan')),
    ('en', _('English')),
]

TIME_ZONE = 'Asia/Baku'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Locale paths
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Whitenoise Configuration for Static File Compression (commented out)
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',  # Disabled - use template views for HTML
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '5/min',     # 5 requests per minute for anonymous users
        'user': '60/min',    # 60 requests per minute for authenticated users
        'login': '5/min',    # 5 login attempts per minute (used for login endpoints)
    },
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# CORS Settings
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://127.0.0.1:3000'
).split(',')

# Cache Configuration
# Using LocMemCache for development (Redis is commented out)
# Redis cache support is optional. Install django-redis and uncomment the block
# below once the dependency is available.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'q360-cache',
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        },
        'TIMEOUT': 300,  # 5 minutes default timeout
    }
}

#  Development Mode: Run tasks synchronously without Redis
if DEBUG:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    CELERY_BROKER_URL = 'memory://'
    CELERY_RESULT_BACKEND = 'cache+memory://'
else:
    # Production Mode: Use Redis for async task processing
    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Redis cache configuration example (install django-redis before enabling).
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             'CONNECTION_POOL_CLASS_KWARGS': {
#                 'max_connections': 50,
#                 'retry_on_timeout': True,
#             },
#             'SOCKET_CONNECT_TIMEOUT': 5,
#             'SOCKET_TIMEOUT': 5,
#         },
#         'KEY_PREFIX': 'q360',
#         'TIMEOUT': 300,  # 5 minutes default timeout
#     }
# }

# Celery Configuration
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Email Configuration
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@q360.gov.az')

# Professional Logging Configuration
# Multi-level logging with rotation, JSON formatting for production monitoring
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # ========== FORMATTERS ==========
    'formatters': {
        # Verbose format for detailed debugging
        'verbose': {
            'format': '[{levelname}] {asctime} | {name}:{lineno} | {funcName} | {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        # Standard format for general logging
        'standard': {
            'format': '[{levelname}] {asctime} | {module} | {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        # Simple format for console
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
        # JSON format for production monitoring and log aggregation
        'json': {
            'format': '{levelname} {asctime} {name} {funcName} {lineno} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },

    # ========== FILTERS ==========
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    # ========== HANDLERS ==========
    'handlers': {
        # Console handler - for development
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose' if DEBUG else 'standard',
            'filters': ['require_debug_true'] if not DEBUG else [],
        },

        # Main application log - rotating file handler
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'q360.log',
            'maxBytes': 1024 * 1024 * 15,  # 15 MB
            'backupCount': 10,  # Keep 10 backup files
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },

        # Error log - separate file for errors only
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'error.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },

        # Security log - authentication, permissions, audit
        'security_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 15,  # Keep more security logs
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },

        # Database log - for query optimization
        'database_file': {
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'database.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },

        # Performance log - slow requests and performance metrics
        'performance_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'performance.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 7,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },

        # API log - REST API calls and responses
        'api_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'api.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 7,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },

        # Celery log - background tasks
        'celery_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'celery.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 7,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },

        # Mail admins on critical errors (production only)
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'verbose',
        },
    },

    # ========== ROOT LOGGER ==========
    'root': {
        'handlers': ['console', 'file', 'error_file'],
        'level': 'INFO',
    },

    # ========== LOGGERS ==========
    'loggers': {
        # Django core loggers
        'django': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },

        # Django request logger - HTTP requests
        'django.request': {
            'handlers': ['file', 'error_file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False,
        },

        # Django database logger - SQL queries
        'django.db.backends': {
            'handlers': ['database_file'] if DEBUG else [],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': False,
        },

        # Django security logger
        'django.security': {
            'handlers': ['security_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },

        # Django server logger
        'django.server': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },

        # Custom app loggers
        'apps.accounts': {
            'handlers': ['file', 'security_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },

        'apps.evaluations': {
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },

        'apps.audit': {
            'handlers': ['file', 'security_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },

        'apps.reports': {
            'handlers': ['file', 'performance_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },

        # REST Framework API logger
        'rest_framework': {
            'handlers': ['api_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },

        # Celery task logger
        'celery': {
            'handlers': ['celery_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },

        'celery.task': {
            'handlers': ['celery_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Security Settings for Production
SECURE_DEFAULTS_ENABLED = not DEBUG

SECURE_SSL_REDIRECT = env_bool('SECURE_SSL_REDIRECT', SECURE_DEFAULTS_ENABLED)
SESSION_COOKIE_SECURE = env_bool('SESSION_COOKIE_SECURE', SECURE_DEFAULTS_ENABLED)
CSRF_COOKIE_SECURE = env_bool('CSRF_COOKIE_SECURE', SECURE_DEFAULTS_ENABLED)
SECURE_BROWSER_XSS_FILTER = env_bool('SECURE_BROWSER_XSS_FILTER', SECURE_DEFAULTS_ENABLED)
SECURE_CONTENT_TYPE_NOSNIFF = env_bool('SECURE_CONTENT_TYPE_NOSNIFF', SECURE_DEFAULTS_ENABLED)
SECURE_CROSS_ORIGIN_OPENER_POLICY = os.getenv('SECURE_CROSS_ORIGIN_OPENER_POLICY', 'same-origin')
SECURE_REFERRER_POLICY = os.getenv(
    'SECURE_REFERRER_POLICY',
    'strict-origin-when-cross-origin' if SECURE_DEFAULTS_ENABLED else 'same-origin'
)
X_FRAME_OPTIONS = os.getenv('X_FRAME_OPTIONS', 'DENY' if SECURE_DEFAULTS_ENABLED else 'SAMEORIGIN')

if SECURE_SSL_REDIRECT:
    # Honour the X-Forwarded-Proto header when running behind a trusted proxy
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '31536000'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', True)
    SECURE_HSTS_PRELOAD = env_bool('SECURE_HSTS_PRELOAD', True)
else:
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '0'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', False)
    SECURE_HSTS_PRELOAD = env_bool('SECURE_HSTS_PRELOAD', False)

# Content Security Policy settings (Updated for django-csp 4.0+)
CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'base-uri': ("'self'",),
        'connect-src': ("'self'", "https://api.example.com"),
        'default-src': ("'self'",),
        'font-src': ("'self'", "https://cdnjs.cloudflare.com"),
        'frame-ancestors': ("'none'",),
        'img-src': ("'self'", "data:", "https:", "https://cdn.tailwindcss.com"),
        'script-src': ("'self'", "'unsafe-inline'", "https://cdn.tailwindcss.com", "https://code.jquery.com", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com"),
        'style-src': ("'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com"),
        'upgrade-insecure-requests': True
    }
}

# Rate limiting for authentication endpoints
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['login'] = '5/min'  # Limit login attempts

# Jazzmin Admin Interface Configuration - Ultra Professional & Modern
JAZZMIN_SETTINGS = {
    # ========== BRANDING ==========
    "site_title": "Q360 Admin Panel",
    "site_header": "Q360 - 360° Performance Management System",
    "site_brand": "Q360",
    "site_logo": None,  # We'll use CSS gradient text instead
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-fluid",
    "site_icon": None,  # Using Font Awesome icon via CSS
    "welcome_sign": "Xoş gəlmisiniz / Welcome",
    "copyright": "Q360 © 2025 - 360° Performance Management System",
    "search_model": ["accounts.User", "evaluations.EvaluationCampaign", "departments.Department"],
    "user_avatar": None,

    # ========== TOP MENU ==========
    "topmenu_links": [
        {"name": "🏠 Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "📊 Analytics", "url": "/reports/analytics/", "permissions": ["auth.view_user"]},
        {"name": "🔒 Security", "url": "/audit/security-dashboard/", "permissions": ["auth.view_user"]},
        {"name": "🌐 Frontend", "url": "/", "new_window": True},
        {"name": "📖 Documentation", "url": "/help/", "new_window": True},
    ],

    # ========== USER MENU ==========
    "usermenu_links": [
        {"name": "👤 My Profile", "url": "/accounts/profile/", "new_window": False},
        {"name": "⚙️ Settings", "url": "/accounts/security/", "new_window": False},
        {"name": "💬 Support", "url": "/admin/support/", "new_window": False},
        {"model": "auth.user"}
    ],

    # ========== SIDEBAR ==========
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],

    # App ordering for better UX
    "order_with_respect_to": [
        "accounts",
        "departments",
        "evaluations",
        "reports",
        "development_plans",
        "competencies",
        "training",
        "recruitment",
        "compensation",
        "leave_attendance",
        "continuous_feedback",
        "workforce_planning",
        "notifications",
        "audit",
        "search",
        "support"
    ],

    # ========== CUSTOM LINKS ==========
    "custom_links": {
        "accounts": [
            {
                "name": "👥 User Management",
                "url": "/admin/accounts/user/",
                "icon": "fas fa-users-cog",
                "permissions": ["accounts.view_user"]
            },
            {
                "name": "🔐 RBAC Matrix",
                "url": "/accounts/rbac-matrix/",
                "icon": "fas fa-shield-alt",
                "permissions": ["accounts.view_user"]
            }
        ],
        "reports": [
            {
                "name": "📊 Analytics Dashboard",
                "url": "/reports/analytics/",
                "icon": "fas fa-chart-line",
                "permissions": ["auth.view_user"]
            },
            {
                "name": "📈 KPI Tracking",
                "url": "/admin/reports/systemkpi/",
                "icon": "fas fa-tachometer-alt",
                "permissions": ["auth.view_user"]
            },
            {
                "name": "🎨 Custom Report Builder",
                "url": "/reports/custom-builder/",
                "icon": "fas fa-magic",
                "permissions": ["auth.view_user"]
            }
        ],
        "evaluations": [
            {
                "name": "📋 My Assignments",
                "url": "/evaluations/my-assignments/",
                "icon": "fas fa-tasks",
            },
            {
                "name": "🎯 Campaign Management",
                "url": "/admin/evaluations/evaluationcampaign/",
                "icon": "fas fa-bullseye",
                "permissions": ["evaluations.view_evaluationcampaign"]
            }
        ]
    },

    # ========== ICONS - Font Awesome 6 ==========
    "icons": {
        # Auth & Permissions
        "auth": "fas fa-shield-halved",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",

        # Accounts
        "accounts": "fas fa-address-card",
        "accounts.User": "fas fa-user-circle",
        "accounts.Profile": "fas fa-id-card",
        "accounts.Role": "fas fa-user-tag",

        # Departments
        "departments": "fas fa-sitemap",
        "departments.Department": "fas fa-building",
        "departments.Position": "fas fa-briefcase",
        "departments.Organization": "fas fa-landmark",

        # Evaluations
        "evaluations": "fas fa-clipboard-check",
        "evaluations.EvaluationCampaign": "fas fa-calendar-check",
        "evaluations.QuestionCategory": "fas fa-folder-open",
        "evaluations.Question": "fas fa-question-circle",
        "evaluations.CampaignQuestion": "fas fa-list-check",
        "evaluations.EvaluationAssignment": "fas fa-tasks",
        "evaluations.Response": "fas fa-comments",
        "evaluations.EvaluationResult": "fas fa-chart-bar",

        # Reports
        "reports": "fas fa-chart-pie",
        "reports.Report": "fas fa-file-chart-line",
        "reports.RadarChartData": "fas fa-radar",
        "reports.SystemKPI": "fas fa-gauge-high",
        "reports.ReportGenerationLog": "fas fa-file-invoice",

        # Notifications
        "notifications": "fas fa-bell",
        "notifications.Notification": "fas fa-bell-on",
        "notifications.EmailTemplate": "fas fa-envelope",

        # Development Plans
        "development_plans": "fas fa-rocket",
        "development_plans.DevelopmentGoal": "fas fa-bullseye",
        "development_plans.GoalProgress": "fas fa-chart-line",
        "development_plans.Objective": "fas fa-target",
        "development_plans.KeyResult": "fas fa-key",

        # Competencies
        "competencies": "fas fa-star",
        "competencies.Competency": "fas fa-award",
        "competencies.UserSkill": "fas fa-user-graduate",

        # Training
        "training": "fas fa-graduation-cap",
        "training.Training": "fas fa-chalkboard-teacher",
        "training.UserTraining": "fas fa-user-check",

        # Recruitment
        "recruitment": "fas fa-user-plus",
        "recruitment.JobPosting": "fas fa-briefcase",
        "recruitment.Application": "fas fa-file-alt",
        "recruitment.Interview": "fas fa-handshake",

        # Compensation
        "compensation": "fas fa-money-bill-wave",
        "compensation.Salary": "fas fa-dollar-sign",
        "compensation.Bonus": "fas fa-gift",

        # Leave & Attendance
        "leave_attendance": "fas fa-calendar-days",
        "leave_attendance.LeaveRequest": "fas fa-plane-departure",
        "leave_attendance.Attendance": "fas fa-clock",

        # Continuous Feedback
        "continuous_feedback": "fas fa-comment-dots",

        # Workforce Planning
        "workforce_planning": "fas fa-users-cog",

        # Audit
        "audit": "fas fa-shield-alt",
        "audit.AuditLog": "fas fa-history",
        "audit.SystemMetric": "fas fa-server",

        # Search
        "search": "fas fa-magnifying-glass",

        # Support
        "support": "fas fa-life-ring",
    },

    # ========== ICON STYLING ==========
    "default_icon_parents": "fas fa-chevron-right",
    "default_icon_children": "fas fa-arrow-right",

    # ========== MODALS & UI ==========
    "related_modal_active": True,  # Enable for better UX

    # ========== CUSTOM CSS & JS ==========
    "custom_css": "css/admin_custom.css",
    "custom_js": "js/admin_enhancements.js",
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,  # Disable UI builder in production

    # ========== FORM LAYOUTS ==========
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "horizontal_tabs",
        "auth.group": "vertical_tabs",
        "accounts.user": "horizontal_tabs",
        "accounts.profile": "collapsible",
        "evaluations.evaluationcampaign": "horizontal_tabs",
        "reports.report": "collapsible",
    },

    # ========== FILTERS ==========
    "show_ui_builder": False,
    "language_chooser": True,

    # ========== WELCOME SCREEN ==========
    "welcome_sign": "Xoş gəlmisiniz!",
    "copyright": "Q360 Performance Management System © 2025",

    # ========== LOGIN PAGE ==========
    "login_logo": None,
    "login_logo_dark": None,
}

JAZZMIN_UI_TWEAKS = {
    # ========== TEXT SIZING ==========
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,

    # ========== COLOR SCHEME (Dark Theme) ==========
    "brand_colour": "navbar-dark",  # Dark navbar for professional look
    "accent": "accent-primary",  # Primary accent color
    "navbar": "navbar-dark",  # Dark navbar
    "no_navbar_border": False,  # Show subtle border

    # ========== LAYOUT ==========
    "navbar_fixed": True,  # Fixed top navbar
    "layout_boxed": False,  # Full-width layout
    "footer_fixed": False,  # Footer scrolls with content

    # ========== SIDEBAR ==========
    "sidebar_fixed": True,  # Fixed sidebar
    "sidebar": "sidebar-dark-primary",  # Dark sidebar with primary accent
    "sidebar_nav_small_text": False,  # Comfortable text size
    "sidebar_disable_expand": False,  # Allow menu expansion
    "sidebar_nav_legacy_style": False,  # Modern sidebar style
    "sidebar_nav_compact_style": False,  # Comfortable spacing
    "sidebar_nav_child_indent": True,  # Indent child items
    "sidebar_nav_flat_style": False,  # Hierarchical structure

    # ========== THEME ==========
    "theme": "darkly",  # Dark theme as base
    "dark_mode_theme": "darkly",  # Dark mode theme

    # ========== BUTTON STYLING ==========
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },

    # ========== ADDITIONAL CUSTOM TWEAKS ==========
    "sidebar_nav_accordion": True,  # Accordion-style menu
}

# Django Channels Configuration (commented out - install channels if needed)
# ASGI_APPLICATION = 'config.asgi.application'

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             'hosts': [os.getenv('REDIS_URL', 'redis://localhost:6379/1')],
#         },
#     },
# }
