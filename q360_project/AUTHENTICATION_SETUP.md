# 🔐 Q360 Autentifikasiya Sistemi - Tam Bələdçi

## 📋 İcmal

Q360 layihəsində tam funksional autentifikasiya sistemi tətbiq edilmişdir. Bu sistem aşağıdakı funksiyaları dəstəkləyir:

✅ **Giriş (Login)** - Email və ya istifadəçi adı ilə
✅ **Qeydiyyat (Registration)** - Tam sahə dəstəyi
✅ **Profil İdarəetməsi** - Görüntüləmə və redaktə
✅ **Şifrəni Unutdum** - Email doğrulama ilə

---

## 🎯 1. Login (Daxil Olma) Səhifəsi

### Xüsusiyyətlər:
- ✉️ **Email VƏ YA istifadəçi adı ilə giriş**
- 🔑 **Şifrə göstərmə/gizlətmə funksiyası**
- ✅ **"Məni xatırla" checkbox**
- 🔁 **"Şifrəni unutmusunuz?" linki**
- 🎨 **Professional animasiyalı dizayn**

### URL:
```
http://localhost:8000/accounts/login/
```

### Backend Tətbiqi:
- **View**: `apps/accounts/template_views.py:19` (login_view)
- **Form**: `apps/accounts/forms.py:11` (UserLoginForm)
- **Template**: `templates/accounts/login.html`
- **Auth Backend**: `apps/accounts/auth_backends.py:12` (EmailOrUsernameBackend)

### Xüsusiyyətlər:
```python
# Email OR Username authentication
User can login with:
- username: "john_doe"
- OR email: "john@example.com"
```

---

## 📝 2. Qeydiyyat (Registration) Səhifəsi

### Məcburi Sahələr:
- 👤 **Ad** (first_name)
- 👤 **Soyad** (last_name)
- 🧑‍💼 **İstifadəçi adı** (username) - unikal
- 📧 **Email ünvanı** (email) - unikal
- 💼 **Vəzifə** (position)
- 🔒 **Şifrə** (password1) - minimum 8 simvol
- 🔒 **Şifrəni təkrar daxil edin** (password2)

### Opsional Sahələr:
- 👔 **Ata adı** (middle_name)
- 🏢 **Şöbə** (department) - dropdown seçim
- 📱 **Əlaqə nömrəsi** (phone_number)
- 📅 **Doğum tarixi** (date_of_birth)

### URL:
```
http://localhost:8000/accounts/register/
```

### Şifrə Tələbləri:
✅ Minimum 8 simvol
✅ Ən azı 1 böyük hərf
✅ Ən azı 1 rəqəm
✅ Ümumi istifadə olunan şifrələr qadağandır

### Form Validasiyası:
- **Email unikallığı** yoxlanılır
- **İstifadəçi adı unikallığı** yoxlanılır
- **Şifrə gücü** real-time göstərilir (Zəif/Orta/Güclü)
- **Şifrə uyğunluğu** yoxlanılır

### Backend Tətbiqi:
- **View**: `apps/accounts/template_views.py:52` (register_view)
- **Form**: `apps/accounts/forms.py:29` (UserRegistrationForm)
- **Template**: `templates/accounts/register.html`
- **Model**: `apps/accounts/models.py:63` (User), `apps/accounts/models.py:224` (Profile)

### Form Save Prosesi:
```python
def save(self, commit=True):
    user = super().save(commit=False)
    user.position = self.cleaned_data.get('position')
    user.department = self.cleaned_data.get('department')
    user.phone_number = self.cleaned_data.get('phone_number', '')

    if commit:
        user.save()
        # Create profile with date_of_birth
        profile, created = Profile.objects.get_or_create(user=user)
        if date_of_birth:
            profile.date_of_birth = date_of_birth
            profile.save()

    return user
```

---

## 👤 3. Profil Səhifəsi

### Görünən Məlumatlar:
- 🧾 **Ad, Soyad, Ata adı**
- ✉️ **Email ünvanı**
- 📞 **Telefon nömrəsi**
- 💼 **Vəzifə və şöbə**
- 📅 **Qeydiyyat tarixi**
- 🎯 **Performans statistikaları**
- 📊 **Ortalama qiymətləndirmə balı**
- 🏆 **Nailiyyətlər**
- 📈 **Kompetensiya radar chart**

### URL-lər:
```
Profil görüntüləmə: http://localhost:8000/accounts/profile/
Profil redaktəsi:    http://localhost:8000/accounts/profile/edit/
Təhlükəsizlik:       http://localhost:8000/accounts/security/
```

### Redaktə Edilə Bilən Sahələr:
- Ad, Soyad, Ata adı
- Email
- Telefon nömrəsi
- Profil şəkli
- Bio
- Doğum tarixi
- İş məlumatları
- Dil seçimi
- Bildiriş tənzimləmələri

### Backend Tətbiqi:
- **View**: `apps/accounts/template_views.py:208` (ProfileView)
- **Update View**: `apps/accounts/template_views.py:262` (ProfileUpdateView)
- **Forms**: `apps/accounts/forms.py:157` (UserUpdateForm), `apps/accounts/forms.py:199` (ProfileUpdateForm)
- **Templates**: `templates/accounts/profile.html`, `templates/accounts/profile_edit.html`

---

## 🔁 4. Şifrəni Unutdum (Forget Password)

### Proses Axını:

#### Addım 1: Email Daxil Et
- İstifadəçi email ünvanını daxil edir
- **URL**: `http://localhost:8000/accounts/password-reset/`

#### Addım 2: Email Göndərilir
- Sistem təhlükəsiz token yaradır
- Professional HTML email göndərilir
- Token 24 saat etibarlıdır

#### Addım 3: Email-dəki Linkə Klik
- İstifadəçi email-dəki linki açır
- Link formatı: `http://localhost:8000/accounts/password-reset/<uidb64>/<token>/`

#### Addım 4: Yeni Şifrə Təyin Et
- İstifadəçi yeni şifrə daxil edir (2 dəfə)
- Şifrə gücü yoxlanılır
- **URL**: `http://localhost:8000/accounts/password-reset/<uidb64>/<token>/`

#### Addım 5: Uğurla Tamamlandı
- Şifrə dəyişdirilir
- İstifadəçi login səhifəsinə yönləndirilir
- **URL**: `http://localhost:8000/accounts/password-reset/complete/`

### Backend Tətbiqi:
- **Views**:
  - `apps/accounts/template_views.py:359` (password_reset_request)
  - `apps/accounts/template_views.py:384` (password_reset_confirm)
  - `apps/accounts/template_views.py:412` (password_reset_complete)
- **Templates**:
  - `templates/accounts/password_reset.html`
  - `templates/accounts/password_reset_done.html`
  - `templates/accounts/password_reset_confirm.html`
  - `templates/accounts/password_reset_complete.html`
  - `templates/accounts/password_reset_email.html`
  - `templates/accounts/password_reset_subject.txt`

### Email Nümunəsi:
```html
Professional HTML email with:
- Q360 branding
- Secure reset button
- Fallback URL link
- Security warning
- 24-hour expiration notice
```

---

## ⚙️ Konfiqurasiya

### 1. Email Tənzimləmələri (Production üçün)

#### Option 1: Gmail SMTP
`config/settings.py` faylında:

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-specific-password'  # Google App Password
DEFAULT_FROM_EMAIL = 'noreply@q360.gov.az'
```

**Gmail üçün App Password yaratmaq:**
1. Google Account → Security
2. 2-Step Verification aktiv edin
3. App Passwords → Select app: Mail → Generate
4. Yaranmış şifrəni `EMAIL_HOST_PASSWORD`-ə əlavə edin

#### Option 2: Azure/Office365 SMTP
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@yourcompany.gov.az'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'noreply@yourcompany.gov.az'
```

#### Option 3: Development üçün (Console Backend)
```python
# Development - emails terminala çap olunur
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### 2. Environment Variables (.env faylı)
Təhlükəsizlik üçün təcrübədə production məlumatlarını environment variables kimi saxlayın:

```bash
# .env faylı yaradın
SECRET_KEY=your-super-secret-key
DEBUG=False

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@q360.gov.az
```

Sonra `config/settings.py`-də:
```python
import os
from pathlib import Path

# Email Configuration
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@q360.gov.az')
```

### 3. Custom Authentication Backend Aktiv Etmə
`config/settings.py` faylında **onsuz da aktivdir**:

```python
# Authentication backends
AUTHENTICATION_BACKENDS = [
    'apps.accounts.auth_backends.EmailOrUsernameBackend',  # Custom backend
    'django.contrib.auth.backends.ModelBackend',  # Default backend
]

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'
```

---

## 🧪 Test Etmək

### 1. Development Server İşə Salın:
```bash
cd q360_project
python manage.py runserver
```

### 2. Test Qeydiyyat:
1. Browser açın: `http://localhost:8000/accounts/register/`
2. Formu doldurun:
   - Ad: Test
   - Soyad: İstifadəçi
   - İstifadəçi adı: testuser
   - Email: test@example.com
   - Vəzifə: Test Menecer
   - Şöbə: Seçin (opsional)
   - Şifrə: Test1234!
3. "Qeydiyyatdan Keç" düyməsinə klikləyin

### 3. Test Login:
1. `http://localhost:8000/accounts/login/`
2. İstifadəçi adı VƏ YA email ilə:
   - `testuser` və ya `test@example.com`
   - Şifrə: Test1234!
3. "Məni xatırla" checkbox-u seçin (opsional)
4. "Daxil Ol" düyməsinə klikləyin

### 4. Test Profil:
1. Uğurlu giriş sonrası: `http://localhost:8000/accounts/profile/`
2. "Profili Redaktə Et" düyməsinə klikləyin
3. Məlumatları dəyişin və saxlayın

### 5. Test Şifrə Sıfırlama:
1. Logout edin
2. Login səhifəsində "Şifrəni unutmusunuz?" klikləyin
3. Email daxil edin: `test@example.com`
4. **Development mode-da**: Terminal-da email linkini görəcəksiniz
5. **Production mode-da**: Real email göndəriləcək

---

## 🔒 Təhlükəsizlik Xüsusiyyətləri

### Tətbiq Edilmiş:
✅ **CSRF Protection** - Bütün formlarda
✅ **Password Hashing** - Django PBKDF2
✅ **Email Validation** - Format və unikallıq
✅ **SQL Injection Prevention** - Django ORM
✅ **XSS Protection** - Template escaping
✅ **Password Strength Validation** - Minimum tələblər
✅ **Rate Limiting** - REST API üçün (5 login/min)
✅ **Session Security** - Secure cookies production-da
✅ **Token-based Password Reset** - 24 saat expiration

### Production Tənzimləmələri (`settings.py`):
```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
```

---

## 📁 Fayl Strukturu

```
q360_project/
├── apps/
│   └── accounts/
│       ├── auth_backends.py        # Email/Username authentication
│       ├── forms.py                 # Login, Registration, Profile forms
│       ├── models.py                # User, Profile, Role models
│       ├── template_views.py        # All view functions
│       ├── urls.py                  # URL routing
│       └── security_utils.py        # Password strength validation
├── templates/
│   └── accounts/
│       ├── login.html               # Login page
│       ├── register.html            # Registration page (NEW)
│       ├── profile.html             # Profile view
│       ├── profile_edit.html        # Profile edit
│       ├── password_reset.html      # Password reset request
│       ├── password_reset_email.html# Email template (HTML)
│       ├── password_reset_subject.txt# Email subject
│       ├── password_reset_done.html # Confirmation page
│       ├── password_reset_confirm.html# New password form
│       └── password_reset_complete.html# Success page
└── config/
    └── settings.py                  # All configurations
```

---

## 🎨 UI/UX Xüsusiyyətləri

### Dizayn Elementləri:
- 🎭 **Animasiyalar**: Fade-in, slide-in, shimmer effektləri
- 🌈 **Gradient backgrounds**: Modern və professional görünüş
- 📱 **Responsive design**: Mobile və desktop uyğun
- ⚡ **Real-time feedback**: Şifrə gücü, form validasiyası
- 🎨 **Icon sistem**: FontAwesome 5 icons
- 🔄 **Loading states**: Smooth transitions
- ✨ **Hover effects**: Interactive elements

### Rəng Palitrası:
- Primary: `#667eea` → `#764ba2` (gradient)
- Success: `#28a745`
- Warning: `#ffc107`
- Danger: `#dc3545`
- Info: `#17a2b8`

---

## 📊 Database Schema

### User Model:
```python
User (AbstractUser):
├── username (unique)
├── email (unique)
├── first_name
├── middle_name
├── last_name
├── role (superadmin/admin/manager/employee)
├── department (ForeignKey)
├── position
├── phone_number
├── profile_picture
├── bio
├── supervisor (ForeignKey to self)
├── is_active
├── date_joined
└── last_login
```

### Profile Model:
```python
Profile (OneToOne with User):
├── date_of_birth
├── place_of_birth
├── nationality
├── hire_date
├── contract_type
├── education_level
├── work_email
├── work_phone
├── address
├── language_preference
├── email_notifications
└── sms_notifications
```

---

## 🚀 Deployment Qeydləri

### Production Checklist:
1. ✅ `DEBUG = False` təyin edin
2. ✅ Email tənzimləmələrini konfiqurasiya edin
3. ✅ `SECRET_KEY` environment variable-a köçürün
4. ✅ `ALLOWED_HOSTS` düzgün təyin edin
5. ✅ SSL/HTTPS aktiv edin
6. ✅ Static faylları collect edin: `python manage.py collectstatic`
7. ✅ Database migration-ları tətbiq edin: `python manage.py migrate`
8. ✅ Superuser yaradın: `python manage.py createsuperuser`

---

## 🛠️ Troubleshooting

### Problem: Email göndərilmir
**Həll**:
- Console backend istifadə edin development üçün
- Gmail App Password düzgün təyin edin
- Firewall email portlarını (587/465) blok etmədiyini yoxlayın

### Problem: "Email already exists" xətası
**Həll**:
- Database-də həmin email-i yoxlayın
- Admin paneldən köhnə istifadəçini silin
- Və ya fərqli email istifadə edin

### Problem: Şifrə reset linki işləmir
**Həll**:
- URL-in 24 saat keçmədiyini yoxlayın
- Link tam kopyalandığını təsdiq edin
- Browser cache-i təmizləyin

### Problem: Profile yaranmır
**Həll**:
- Qeydiyyat formu yeni profil avtomatik yaradır
- Əgər yoxdursa: Django Admin → Profiles → Add Profile

---

## 📞 Dəstək

Suallar üçün:
- 📧 Email: support@q360.gov.az
- 📚 Dokumentasiya: `/help` səhifəsi
- 🔧 Admin Panel: `http://localhost:8000/admin/`

---

## ✅ Tamamlanmış Xüsusiyyətlər

✅ Login səhifəsi (email və username dəstəyi ilə)
✅ Qeydiyyat səhifəsi (tam sahə dəstəyi)
✅ Profil görüntüləmə
✅ Profil redaktəsi
✅ Şifrəni unutdum prosesi
✅ Email doğrulama
✅ Şifrə gücü yoxlaması
✅ Form validasiyası
✅ Professional UI/UX dizayn
✅ Responsive mobil dəstək
✅ Təhlükəsizlik xüsusiyyətləri

---

**Son yeniləmə**: {{ now }}
**Version**: 1.0.0
**Status**: ✅ Production Ready
