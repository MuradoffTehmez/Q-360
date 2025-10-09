# Django i18n Configuration for Q360 Project
# Add these settings to your settings.py file

from django.utils.translation import gettext_lazy as _

# Internationalization
LANGUAGE_CODE = 'az'  # Default language

LANGUAGES = [
    ('az', _('Azərbaycan')),
    ('en', _('English')),
]

# Enable i18n
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Locale paths
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Middleware - Add LocaleMiddleware after SessionMiddleware
# MIDDLEWARE = [
#     ...
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.locale.LocaleMiddleware',  # Add this line
#     'django.middleware.common.CommonMiddleware',
#     ...
# ]

# Template context processors - Make sure these are included
# 'TEMPLATES': [{
#     'OPTIONS': {
#         'context_processors': [
#             ...
#             'django.template.context_processors.i18n',
#             ...
#         ],
#     },
# }]
