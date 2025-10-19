# Q360 - 360 Dərəcə Qiymətləndirmə Sistemi

Dövlət sektoru üçün nəzərdə tutulmuş peşəkar 360 dərəcə qiymətləndirmə platforması.

## 📋 Layihə Haqqında

Q360, dövlət qurumlarında (nazirliklər, idarələr, şöbələr) işçilərin performansının hərtərəfli, obyektiv və çox-mənbəli rəy mexanizmi ilə qiymətləndirilməsi üçün nəzərdə tutulmuş tam funksional HR qiymətləndirmə sistemidir.

### Əsas Xüsusiyyətlər

- ✅ **360° Qiymətləndirmə**: Özünüdəyərləndirmə, rəhbər, həmkar və tabelik qiymətləndirməsi
- ✅ **Kampaniya İdarəetməsi**: Qiymətləndirmə dövrlərinin təşkili və idarəsi
- ✅ **Anonim Rəylər**: İşçilərin anonim qiymətləndirməsi
- ✅ **Avtomatik Hesabatlar**: PDF və Excel formatında hesabat generasiyası
- ✅ **Radar Qrafiklər**: Vizual kompetensiya analizi
- ✅ **Fərdi İnkişaf Planı (IDP)**: Performans əsaslı inkişaf məqsədləri
- ✅ **Audit Sistemi**: Bütün sistem hərəkətlərinin qeydiyyatı
- ✅ **Rol Əsaslı İcazələr**: SuperAdmin, Admin, Menecer, İşçi rolları

## 🛠️ Texnoloji Stack

### Backend
- **Framework**: Django 5.1+ & Django REST Framework
- **Verilənlər Bazası**: PostgreSQL 16
- **Asinxron Tapşırıqlar**: Celery + Redis
- **Autentifikasiya**: JWT (Simple JWT)
- **Audit**: Django Simple History

### Deployment
- **Container**: Docker & Docker Compose
- **Web Server**: Nginx
- **WSGI Server**: Gunicorn
- **Environment**: Python 3.12+

## 🚀 Quraşdırma

### Tələblər
- Docker ve Docker Compose
- Git

### Addım-addım Quraşdırma

1. **Layihəni klonlayın**
```bash
git clone <repository-url>
cd q360_project
```

2. **Environment faylını yaradın**
```bash
cp .env.example .env
```

3. **.env faylını konfiqurasiya edin**
```bash
# SECRET_KEY, DB_PASSWORD və digər parametrləri dəyişdirin
nano .env
```

4. **Docker konteynerləri qaldırın**
```bash
docker-compose up -d --build
```

5. **Migrationsları icra edin**
```bash
docker-compose exec web python manage.py migrate
```

6. **Superuser yaradın**
```bash
docker-compose exec web python manage.py createsuperuser
```

7. **Statik faylları yığın**
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

## 📦 Servisler

Sistem aşağıdakı servislər üzərində işləyir:

- **Web Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/api
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Nginx**: http://localhost

## 🔑 API Endpoints

### Autentifikasiya
```
POST /api/auth/token/          # Token əldə et
POST /api/auth/token/refresh/  # Token yenilə
POST /api/auth/token/verify/   # Token yoxla
```

### İstifadəçilər
```
GET    /api/accounts/users/           # İstifadəçi siyahısı
POST   /api/accounts/users/           # Yeni istifadəçi
GET    /api/accounts/users/{id}/      # İstifadəçi detalları
PUT    /api/accounts/users/{id}/      # İstifadəçi yenilə
DELETE /api/accounts/users/{id}/      # İstifadəçi sil
GET    /api/accounts/users/me/        # Cari istifadəçi
```

### Qiymətləndirmə Kampaniyaları
```
GET    /api/evaluations/campaigns/       # Kampaniya siyahısı
POST   /api/evaluations/campaigns/       # Yeni kampaniya
GET    /api/evaluations/campaigns/{id}/  # Kampaniya detalları
POST   /api/evaluations/campaigns/{id}/activate/   # Aktivləşdir
POST   /api/evaluations/campaigns/{id}/complete/   # Tamamla
```

### Tapşırıqlar və Cavablar
```
GET    /api/evaluations/assignments/     # Qiymətləndirmə tapşırıqları
POST   /api/evaluations/responses/       # Cavab göndər
GET    /api/evaluations/results/         # Nəticələr
```

## 📊 Strukturun Quruluşu

```
q360_project/
├── config/                 # Django konfiqurasiya faylları
│   ├── settings.py        # Əsas parametrlər
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI konfiqurasiyası
│   └── celery.py          # Celery konfiqurasiyası
├── apps/                  # Django tətbiqləri
│   ├── accounts/          # İstifadəçi idarəetməsi
│   ├── departments/       # Təşkilat strukturu
│   ├── evaluations/       # Qiymətləndirmə sistemi
│   ├── notifications/     # Bildiriş sistemi
│   ├── reports/           # Hesabat generasiyası
│   ├── development_plans/ # İnkişaf planları
│   └── audit/             # Audit qeydləri
├── static/                # Statik fayllar
├── media/                 # Yüklənmiş fayllar
├── templates/             # HTML şablonları
├── nginx/                 # Nginx konfiqurasiyası
├── Dockerfile             # Docker image təsviri
├── docker-compose.yml     # Docker servis konfiqurasiyası
├── requirements.txt       # Python paketləri
└── manage.py              # Django menecment komandaları
```

## 🧪 Development

### Lokal İnkişaf Mühiti

```bash
# Virtual environment yaradın
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Paketləri quraşdırın
pip install -r requirements.txt

# Migrationslar
python manage.py makemigrations
python manage.py migrate

# Development server
python manage.py runserver

# Celery worker (ayrı terminalda)
celery -A config worker -l info

# Celery beat (ayrı terminalda)
celery -A config beat -l info
```

### Test Komandaları

```bash
# Bütün testlər
python manage.py test

# Specific app test
python manage.py test apps.evaluations

# Coverage report
coverage run manage.py test
coverage report
```

## 👥 İstifadəçi Rolları

1. **SuperAdmin**: Sistem üzrə tam nəzarət
2. **Admin**: Təşkilat səviyyəsində idarəetmə
3. **Menecer**: Komanda qiymətləndirməsi və hesabatlar
4. **İşçi**: Qiymətləndirmə formaları və fərdi hesabat

## 🔒 Təhlükəsizlik

- ✅ HTTPS məcburi (production)
- ✅ JWT token əsaslı autentifikasiya
- ✅ CSRF protection
- ✅ SQL Injection qorunması
- ✅ XSS prevention
- ✅ Rol əsaslı icazə sistemi (RBAC)
- ✅ Şifrələrin hash edilməsi (PBKDF2/Argon2)
- ✅ Environment secrets
- ✅ Rate limiting (API throttling)

## 📝 Qeydlər

### İlk İstifadə

1. Admin panelə daxil olun: `/admin`
2. Təşkilat və şöbələri yaradın
3. İstifadəçiləri əlavə edin
4. Sual kateqoriyaları və sualları müəyyən edin
5. Qiymətləndirmə kampaniyası yaradın
6. İstifadəçilərə tapşırıqlar təyin edin
7. Kampaniyanı aktivləşdirin

### Celery Tasks

- E-poçt göndərilməsi
- Hesabat generasiyası
- Kampaniya bildirişləri
- Avtomatik xatırlatmalar

## 🤝 Töhfə

Bu layihə dövlət sektoru üçün nəzərdə tutulmuşdur. Töhfələr və təkliflər üçün issue açın.

## 📄 Lisenziya

Bu layihə dövlət qurumlarının istifadəsi üçün yaradılmışdır.

## 📞 Əlaqə

Texniki dəstək və suallar üçün layihə meneceri ilə əlaqə saxlayın.

---

**© 2025 Q360 Evaluation System - Dövlət Qulluqçuları üçün 360° Qiymətləndirmə Platforması**
