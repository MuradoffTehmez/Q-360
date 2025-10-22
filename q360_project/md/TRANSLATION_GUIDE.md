# Q360 Translation Guide

## İstifadə Təlimatı / Usage Instructions

### 1. Django Tənzimləmələri / Django Settings

`settings.py` faylınıza aşağıdakı ayarları əlavə edin:

```python
from django.utils.translation import gettext_lazy as _

# Internationalization
LANGUAGE_CODE = 'az'  # Default language

LANGUAGES = [
    ('az', _('Azərbaycan')),
    ('en', _('English')),
]

USE_I18N = True
USE_L10N = True

# Locale paths
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Middleware - Add LocaleMiddleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Add this line
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Template context processors
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.template.context_processors.i18n',  # Make sure this is included
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]
```

### 2. URL Configuration

`urls.py` faylınıza dil dəyişdirmə URL-ni əlavə edin:

```python
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.views.i18n import set_language

urlpatterns = [
    path('i18n/setlang/', set_language, name='set_language'),
    # Your other URL patterns
]
```

### 3. Tərcümə Fayllarını Yaratmaq / Creating Translation Files

Terminal-da aşağıdakı əmrləri icra edin:

```bash
# Bütün template-lərdə tərcümə ediləcək mətnləri tap
python manage.py makemessages -l az
python manage.py makemessages -l en

# JavaScript faylları üçün (əgər varsa)
python manage.py makemessages -d djangojs -l az
python manage.py makemessages -d djangojs -l en
```

### 4. Tərcümə Etmək / Translating

1. `locale/az/LC_MESSAGES/django.po` faylını açın
2. `locale/en/LC_MESSAGES/django.po` faylını açın
3. Her `msgid` üçün müvafiq `msgstr` yazın

Nümunə / Example:
```po
msgid "Home"
msgstr "Əsas Səhifə"  # Azərbaycan dilində

msgid "Home"
msgstr "Home"  # İngilis dilində (eyni)
```

### 5. Tərcümələri Kompilyasiya Etmək / Compiling Translations

```bash
python manage.py compilemessages
```

### 6. Template-lərdə İstifadə / Using in Templates

```django
{% load i18n %}

{# Sadə tərcümə #}
<h1>{% trans "Welcome" %}</h1>

{# Dəyişənli tərcümə #}
{% blocktrans with name=user.name %}
Hello {{ name }}!
{% endblocktrans %}

{# Plural formalar #}
{% blocktrans count counter=list|length %}
There is {{ counter }} item.
{% plural %}
There are {{ counter }} items.
{% endblocktrans %}
```

### 7. Python Kodunda İstifadə / Using in Python Code

```python
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

# Views-da
def my_view(request):
    message = _("This is a translated message")

# Models-da (lazy translation)
class MyModel(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=gettext_lazy("Name")
    )
```

## Tez-tez Tərcümə Olunan Kəlmələr / Common Translations

| English | Azərbaycan |
|---------|-----------|
| Home | Əsas Səhifə |
| Dashboard | İdarə Paneli |
| Profile | Profil |
| Settings | Tənzimləmələr |
| Security | Təhlükəsizlik |
| Notifications | Bildirişlər |
| Logout | Çıxış |
| Login | Giriş |
| Save | Saxla |
| Cancel | Ləğv et |
| Delete | Sil |
| Edit | Redaktə et |
| Create | Yarat |
| Update | Yenilə |
| Search | Axtar |
| Filter | Filtrlə |
| Reports | Hesabatlar |
| Evaluations | Qiymətləndirmələr |
| Campaigns | Kampaniyalar |
| Users | İstifadəçilər |
| Departments | Şöbələr |
| Questions | Suallar |
| Management | İdarəetmə |
| My Assignments | Mənim Tapşırıqlarım |
| All | Hamısı |
| No notifications | Bildiriş yoxdur |
| New Campaign | Yeni Kampaniya |
| Admin Panel | Admin Panel |

## Faydalı Əmrlər / Useful Commands

```bash
# Yeni tərcümələri əlavə et
python manage.py makemessages -a

# Mövcud tərcümələri yenilə
python manage.py makemessages -a --no-obsolete

# Tərcümələri kompilyasiya et
python manage.py compilemessages

# Mətn mesajlarını təmizlə
python manage.py makemessages -a --ignore=env
```

## Qeydlər / Notes

1. **Həmişə `{% load i18n %}` əlavə edin** - Hər template faylının əvvəlinə
2. **`gettext_lazy` istifadə edin** - Models və forms-da
3. **Tərcümələri yeniləyin** - Yeni mətn əlavə etdikdə makemessages çağırın
4. **Kompilyasiya etməyi unutmayın** - Dəyişikliklər görünməsi üçün
5. **Dil seçimini test edin** - Hər iki dildə səhifələri yoxlayın

## Dil Seçici Komponent / Language Switcher Component

Dil seçici hər səhifənin yuxarı sağ küncdə yerləşir və istifadəçilərə Azərbaycan və İngilis dilləri arasında asanlıqla keçid etməyə imkan verir.

Komponent: `templates/components/language_switcher.html`
