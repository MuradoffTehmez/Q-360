# Add this to your main urls.py file

from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.views.i18n import set_language

urlpatterns = [
    # Language switcher
    path('i18n/setlang/', set_language, name='set_language'),

    # Add your other URL patterns here
    # Or wrap them in i18n_patterns() for URL translation
]

# Example with i18n_patterns:
# urlpatterns += i18n_patterns(
#     path('', include('your_app.urls')),
# )
