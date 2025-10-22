# Q360 i18n (Beynəlmiləlləşdirmə) Tətbiq Təlimatı

## Hazırlıq İşləri

### 1. Django Tənzimləmələri

`config/settings.py` faylını açın və aşağıdakı dəyişiklikləri edin:

```python
# Faylın əvvəlinə əlavə edin
from django.utils.translation import gettext_lazy as _

# LANGUAGE_CODE dəyişdirin
LANGUAGE_CODE = 'az'  # Əsas dil Azərbaycan dili

# LANGUAGES əlavə edin (LANGUAGE_CODE-dan sonra)
LANGUAGES = [
    ('az', _('Azərbaycan')),
    ('en', _('English')),
]

# Bu ayarların aktiv olduğuna əmin olun
USE_I18N = True
USE_L10N = True

# Locale path əlavə edin
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# MIDDLEWARE-ə LocaleMiddleware əlavə edin
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # ← Bu sətri əlavə edin
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# TEMPLATES-də context_processors yoxlayın
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',  # ← Bu olmalıdır
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### 2. URL Configuration

Əsas `urls.py` faylınıza (məsələn, `config/urls.py`) dil dəyişdirmə URL-ni əlavə edin:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

urlpatterns = [
    # Dil dəyişdirmə URL-i (i18n_patterns-dən kənarda olmalıdır)
    path('i18n/setlang/', set_language, name='set_language'),

    # Admin
    path('admin/', admin.site.urls),

    # Digər URL-lər...
]

# Əgər URL-ləri tərcümə etmək istəyirsinizsə (optional):
# urlpatterns += i18n_patterns(
#     path('', include('your_app.urls')),
# )
```

## Tətbiq Addımları

### Addım 1: Template Fayllarını Yeniləmək

Hər template faylının əvvəlinə `{% load i18n %}` əlavə edin və mətnləri tərcümə teqləri ilə əhatə edin.

**Nümunə - sidebar.html:**

```django
{% load static %}
{% load i18n %}

<nav id="sidebar" class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse">
    <div class="position-sticky pt-3">
        <ul class="nav flex-column">
            <li class="nav-item">
                <a class="nav-link" href="{% url 'dashboard' %}">
                    <i class="fas fa-home me-2"></i> {% trans "Home" %}
                </a>
            </li>

            <li class="nav-item">
                <h6 class="sidebar-heading px-3 mt-4 mb-1 text-muted">
                    <span>{% trans "Evaluations" %}</span>
                </h6>
            </li>
            <!-- və s. -->
        </ul>
    </div>
</nav>
```

### Addım 2: Tərcümə Fayllarını Yaratmaq

Terminal-da proyekt qovluğunda bu əmri icra edin:

```bash
# Əsas qovluğa keçin
cd C:\lahiyeler\q360\q360_project

# Tərcümə fayllarını yarat
python manage.py makemessages -l az
python manage.py makemessages -l en

# Əgər JavaScript fayllarınız varsa
python manage.py makemessages -d djangojs -l az
python manage.py makemessages -d djangojs -l en
```

Bu əmr `locale/az/LC_MESSAGES/django.po` və `locale/en/LC_MESSAGES/django.po` fayllarını yaradacaq və ya yeniləyəcək.

### Addım 3: Tərcümələri Doldurmaq

`locale/az/LC_MESSAGES/django.po` və `locale/en/LC_MESSAGES/django.po` fayllarını açın.

**Azərbaycan dilində (az/LC_MESSAGES/django.po):**
```po
msgid "Home"
msgstr "Əsas Səhifə"

msgid "Profile"
msgstr "Profil"

msgid "Settings"
msgstr "Tənzimləmələr"
```

**İngilis dilində (en/LC_MESSAGES/django.po):**
```po
msgid "Home"
msgstr "Home"

msgid "Profile"
msgstr "Profile"

msgid "Settings"
msgstr "Settings"
```

### Addım 4: Tərcümələri Kompilyasiya Etmək

```bash
python manage.py compilemessages
```

Bu əmr `.po` fayllarından `.mo` faylları yaradacaq (Django-nun istifadə etdiyi format).

### Addım 5: Serveri Yenidən Başlatmaq

```bash
python manage.py runserver
```

## Template Fayllarını Yeniləmək - Ətraflı Nümunələr

### 1. Sadə Mətn Tərcüməsi

```django
{% load i18n %}

<h1>{% trans "Welcome" %}</h1>
<p>{% trans "This is a simple text" %}</p>
```

### 2. Dəyişənli Tərcümə

```django
{% load i18n %}

{% blocktrans with name=user.name %}
Hello {{ name }}!
{% endblocktrans %}

{% blocktrans with count=items|length %}
You have {{ count }} items.
{% endblocktrans %}
```

### 3. Plural Formalar

```django
{% load i18n %}

{% blocktrans count counter=items|length %}
There is {{ counter }} item.
{% plural %}
There are {{ counter }} items.
{% endblocktrans %}
```

### 4. HTML Atributlarında Tərcümə

```django
{% load i18n %}

<input type="text" placeholder="{% trans 'Search...' %}">
<a href="#" title="{% trans 'Click here' %}">{% trans "Link" %}</a>
```

## Prioritet: Yenilənməli Fayllar

### Yüksək Prioritet (Əvvəlcə bunları yeniləyin):

1. ✅ `templates/base/base.html` - TAMAMLANDI
2. ✅ `templates/base/navbar.html` - TAMAMLANDI
3. `templates/base/sidebar.html` - GÖZLƏYİR
4. `templates/landing.html` - GÖZLƏYİR
5. `templates/accounts/login.html` - GÖZLƏYİR

### Orta Prioritet:

6. `templates/accounts/profile.html`
7. `templates/accounts/preferences.html`
8. `templates/accounts/security.html`
9. `templates/notifications/inbox.html`
10. `templates/notifications/detail.html`

### Aşağı Prioritet:

11. `templates/evaluations/self_assessment.html`
12. `templates/reports/enhanced_report.html`
13. Digər səhifələr

## Python Kodunda Tərcümə

### Views-da

```python
from django.utils.translation import gettext as _

def my_view(request):
    message = _("This message will be translated")
    messages.success(request, message)
```

### Models-da

```python
from django.utils.translation import gettext_lazy as _

class MyModel(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name")
    )

    class Meta:
        verbose_name = _("My Model")
        verbose_name_plural = _("My Models")
```

### Forms-da

```python
from django.utils.translation import gettext_lazy as _

class MyForm(forms.Form):
    name = forms.CharField(
        label=_("Name"),
        help_text=_("Enter your name")
    )
```

## Test Etmək

1. Serveri işə salın: `python manage.py runserver`
2. Brauzerdə açın: `http://localhost:8000`
3. Yuxarı sağ küncdə dil seçicidən AZ və EN arasında keçid edin
4. Səhifələrin tərcümə edildiyini yoxlayın

## Problemlərin Həlli

### Problem: Tərcümələr görünmür

**Həll:**
1. `python manage.py compilemessages` əmrini çağırdığınızdan əmin olun
2. Serveri yenidən başladın
3. Brauzer cache-ni təmizləyin (Ctrl+Shift+R)

### Problem: Yeni mətnlər .po faylında yoxdur

**Həll:**
```bash
python manage.py makemessages -a --no-obsolete
python manage.py compilemessages
```

### Problem: LocaleMiddleware işləmir

**Həll:**
- `settings.py`-də SessionMiddleware-dən SONRA olmalıdır
- `LANGUAGES` və `LANGUAGE_CODE` düzgün təyin edilməlidir

## Faydalı Əmrlər

```bash
# Bütün dillərdə mesajları yenilə
python manage.py makemessages -a

# Köhnə tərcümələri çıxar
python manage.py makemessages -a --no-obsolete

# Spesifik qovluqları ignore et
python manage.py makemessages -a --ignore=venv --ignore=env

# Tərcümələri kompilyasiya et
python manage.py compilemessages

# Spesifik dil üçün
python manage.py compilemessages -l az
```

## Növbəti Addımlar

1. ✅ Dil seçici komponent yaradıldı
2. ✅ Base template və navbar yeniləndi
3. 📝 Sidebar-ı yeniləyin (növbəti addım)
4. 📝 Landing page-i yeniləyin
5. 📝 Digər template fayllarını yeniləyin
6. 📝 `makemessages` və `compilemessages` çağırın
7. 📝 Test edin və yoxlayın

## Əlavə Qaynaqlar

- Django i18n dokumentasiyası: https://docs.djangoproject.com/en/4.2/topics/i18n/
- Translation Best Practices: https://docs.djangoproject.com/en/4.2/topics/i18n/translation/
