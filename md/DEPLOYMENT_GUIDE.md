# Q360 Yeni Modullar - Deployment Təlimatı

## 📝 Ümumi Məlumat

Bu təlimat yeni yaradılmış 3 modulun (Competencies, Training, Security) sistemə inteqrasiyası və test edilməsi üçün addım-addım göstərişlər verir.

---

## 🔧 Addım 1: Migration-ların Yaradılması və Tətbiqi

### 1.1 Migration Fayllarını Yaratmaq

```bash
python manage.py makemigrations competencies
python manage.py makemigrations training
python manage.py makemigrations audit
```

**Gözlənilən nəticə:**
```
Migrations for 'competencies':
  apps\competencies\migrations\0001_initial.py
    - Create model Competency
    - Create model ProficiencyLevel
    - Create model PositionCompetency
    - Create model UserSkill
    - Create model HistoricalCompetency
    ...

Migrations for 'training':
  apps\training\migrations\0001_initial.py
    - Create model TrainingResource
    - Create model UserTraining
    ...

Migrations for 'audit':
  apps\audit\migrations\000X_add_login_failure.py
    - Alter field action in auditlog
```

### 1.2 Migration-ları Tətbiq Etmək

```bash
python manage.py migrate
```

**Gözlənilən nəticə:**
```
Running migrations:
  Applying competencies.0001_initial... OK
  Applying training.0001_initial... OK
  Applying audit.000X_add_login_failure... OK
```

---

## 📊 Addım 2: İlkin Məlumatların Yaradılması

### 2.1 ProficiencyLevel-ləri Yaratmaq

Django shell-i açın:
```bash
python manage.py shell
```

Aşağıdakı kodu icra edin:
```python
from apps.competencies.models import ProficiencyLevel

# Mövcud məlumatları yoxlayın
if ProficiencyLevel.objects.count() == 0:
    # 4 səviyyə yaradın
    ProficiencyLevel.objects.create(
        name='basic',
        score_min=0,
        score_max=25
    )
    ProficiencyLevel.objects.create(
        name='intermediate',
        score_min=26,
        score_max=50
    )
    ProficiencyLevel.objects.create(
        name='advanced',
        score_min=51,
        score_max=75
    )
    ProficiencyLevel.objects.create(
        name='expert',
        score_min=76,
        score_max=100
    )
    print("✅ 4 ProficiencyLevel yaradıldı")
else:
    print(f"⚠️ Artıq {ProficiencyLevel.objects.count()} ProficiencyLevel mövcuddur")

# Yoxlama
for level in ProficiencyLevel.objects.all():
    print(f"  - {level.name}: {level.score_min}-{level.score_max}")

# Shell-dən çıxın
exit()
```

### 2.2 Demo Kompetensiyalar Yaratmaq (İstəyə görə)

```python
from apps.competencies.models import Competency

competencies = [
    {
        'name': 'Python Proqramlaşdırma',
        'description': 'Python dilində proqramlaşdırma bacarıqları'
    },
    {
        'name': 'Django Framework',
        'description': 'Django web framework-ündə development'
    },
    {
        'name': 'SQL və Database İdarəetməsi',
        'description': 'Verilənlər bazası dizaynı və optimallaşdırma'
    },
    {
        'name': 'REST API Dizaynı',
        'description': 'RESTful API layihələndirmə və implementasiya'
    },
    {
        'name': 'Frontend Development',
        'description': 'HTML, CSS, JavaScript ilə frontend development'
    }
]

for comp_data in competencies:
    comp, created = Competency.objects.get_or_create(
        name=comp_data['name'],
        defaults={'description': comp_data['description']}
    )
    if created:
        print(f"✅ Yaradıldı: {comp.name}")
    else:
        print(f"⚠️ Mövcuddur: {comp.name}")
```

### 2.3 Demo Təlim Resursları Yaratmaq (İstəyə görə)

```python
from apps.training.models import TrainingResource
from apps.competencies.models import Competency

# Python kompetensiyası üçün təlim
python_comp = Competency.objects.get(name='Python Proqramlaşdırma')

training = TrainingResource.objects.create(
    title='Advanced Python Programming',
    type='course',
    description='Təkmil Python proqramlaşdırma kursu',
    provider='Udemy',
    duration_hours=40,
    difficulty_level='intermediate',
    cost=99.00,
    external_link='https://www.udemy.com/course/python-advanced'
)
training.required_competencies.add(python_comp)
print(f"✅ Yaradıldı: {training.title}")
```

---

## 🚀 Addım 3: Celery və Redis Quraşdırma

### 3.1 Redis Quraşdırma (Windows)

**Variant 1: Windows üçün Redis endirmək**
```bash
# Memurai Redis for Windows (tövsiyə edilir)
https://www.memurai.com/get-memurai

# Və ya WSL ilə Redis
wsl --install
wsl
sudo apt update
sudo apt install redis-server
sudo service redis-server start
```

**Redis test:**
```bash
redis-cli ping
# Cavab: PONG
```

### 3.2 Celery Worker İşə Salmaq

**Terminal 1 - Worker:**
```bash
celery -A config worker -l info --pool=solo
```

**Terminal 2 - Beat (periodic tasks üçün):**
```bash
celery -A config beat -l info
```

**Gözlənilən nəticə:**
```
-------------- celery@HOSTNAME v5.x.x
---- **** -----
--- * ***  * -- Windows-10
-- * - **** ---
- ** ----------
[tasks]
  . training.assign_training_for_development_goal
  . training.send_training_due_reminders
  . training.recommend_trainings_for_user
  . training.update_user_skill_stats

[2025-10-11 10:00:00,000: INFO/MainProcess] Connected to redis://localhost:6379/0
[2025-10-11 10:00:00,000: INFO/MainProcess] celery ready.
```

---

## 🌐 Addım 4: Development Server İşə Salmaq

```bash
python manage.py runserver
```

Server işə düşdükdən sonra:
```
Starting development server at http://127.0.0.1:8000/
```

---

## ✅ Addım 5: API Endpoint-lərini Test Etmək

### 5.1 Admin Paneldən Giriş

```
http://localhost:8000/admin/
```

Admin istifadəçi ilə giriş edin və yoxlayın:
- Competencies bölməsində model-lər görünür
- Training bölməsində model-lər görünür
- Audit bölməsində AuditLog mövcuddur

### 5.2 API Token Almaq

**Postman və ya curl ilə:**
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "yourpassword"}'
```

**Cavab:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 5.3 API Endpoint Test-ləri

**Kompetensiyalar:**
```bash
# Siyahı
curl http://localhost:8000/api/competencies/api/competencies/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Statistika
curl http://localhost:8000/api/competencies/api/competencies/statistics/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Mənim bacarıqlarım
curl http://localhost:8000/api/competencies/api/user-skills/my_skills/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Training:**
```bash
# Resurslar
curl http://localhost:8000/api/training/api/resources/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Pending təlimlər
curl http://localhost:8000/api/training/api/user-trainings/my_pending/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Security:**
```bash
# Təhlükəsizlik statistikaları
curl http://localhost:8000/api/audit/api/security-stats/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🎨 Addım 6: Frontend Səhifələrini Test Etmək

### 6.1 Giriş Edin

```
http://localhost:8000/accounts/login/
```

### 6.2 Səhifələri Ziyarət Edin

**Kompetensiyalar:**
```
http://localhost:8000/competencies/
http://localhost:8000/competencies/my-skills/
```

**Training:**
```
http://localhost:8000/training/
http://localhost:8000/training/catalog/
```

**Security (Admin only):**
```
http://localhost:8000/audit/security/
```

### 6.3 Yoxlama Listi

- [ ] Səhifələr yüklənir (500 error yoxdur)
- [ ] Navigation menu işləyir
- [ ] AJAX requestlər işləyir (browser console-da error yoxdur)
- [ ] Formlar submit olunur
- [ ] Modal-lar açılır
- [ ] Qrafiklər render olunur (Chart.js)
- [ ] Responsive design işləyir (mobil görünüş)

---

## 🐛 Troubleshooting

### Problem 1: Migration Error

**Xəta:**
```
django.db.utils.OperationalError: no such table: competencies_competency
```

**Həll:**
```bash
python manage.py migrate --run-syncdb
```

### Problem 2: Celery Connection Error

**Xəta:**
```
[ERROR/MainProcess] consumer: Cannot connect to redis://localhost:6379/0
```

**Həll:**
1. Redis işə salındığını yoxlayın: `redis-cli ping`
2. `config/settings.py`-də CELERY_BROKER_URL yoxlayın

### Problem 3: Static Files 404

**Xəta:**
Bootstrap/Chart.js yüklənmir

**Həll:**
```bash
python manage.py collectstatic
```

Və ya CDN linklərini yoxlayın templates-də.

### Problem 4: CORS Error (Frontend)

**Xəta:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Həll:**
`config/settings.py`-də:
```python
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware'] + MIDDLEWARE
CORS_ALLOW_ALL_ORIGINS = True  # Development üçün
```

### Problem 5: 403 Forbidden (API)

**Xəta:**
```
{"detail": "Authentication credentials were not provided."}
```

**Həll:**
- JWT token-in düzgün göndərildiyini yoxlayın
- Header: `Authorization: Bearer YOUR_TOKEN`

---

## 📊 Test Ssenariləri

### Ssenarı 1: İstifadəçi Bacarıq Əlavə Edir

1. Login olun
2. `/competencies/my-skills/` səhifəsinə gedin
3. "Add Skill" düyməsinə klikləyin
4. Modal-da kompetensiya və level seçin
5. "Add" düyməsinə basın
6. Yeni bacarıq siyahıda görünməlidir

### Ssenarı 2: Manager Bacarığı Təsdiq Edir

1. Manager kimi login olun
2. Admin panel: `/admin/competencies/userskill/`
3. Pending statuslu bacarıq seçin
4. "Approve selected skills" action-ını seçin
5. Bacarıq status-u "approved" olmalıdır

### Ssenarı 3: Admin Təlim Təyin Edir

1. Admin kimi login olun
2. Admin panel: `/admin/training/usertraining/add/`
3. İstifadəçi və təlim resurs seçin
4. Status "pending" olaraq saxlayın
5. İstifadəçiyə notification göndərilməlidir (Celery)

### Ssenarı 4: Təhlükəsizlik Dashboard

1. Admin kimi login olun
2. `/audit/security/` səhifəsinə gedin
3. Qrafik görünməlidir
4. Uğursuz giriş cəhdi edin (logout + wrong password)
5. Dashboard-da statistika yenilənməlidir

---

## ✨ Production Hazırlıq

### 1. Environment Variables

`.env` faylı yaradın:
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DATABASE_URL=postgresql://user:password@localhost:5432/q360_db

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### 2. Static Files

```bash
python manage.py collectstatic --noinput
```

### 3. Security Checks

```bash
python manage.py check --deploy
```

### 4. Gunicorn (Linux/Production)

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### 5. Nginx Configuration (Nümunə)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/q360/staticfiles/;
    }

    location /media/ {
        alias /path/to/q360/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📞 Dəstək

Problemlə qarşılaşdıqda:

1. **Logları yoxlayın:**
   - Django: Terminal output
   - Celery: Celery worker terminal
   - Redis: `redis-cli monitor`

2. **Browser Console:**
   - F12 → Console tab
   - Network tab (AJAX errors)

3. **Django Debug Toolbar:**
   ```python
   # settings.py
   if DEBUG:
       INSTALLED_APPS += ['debug_toolbar']
   ```

---

**Deployment təlimatı hazırlanma tarixi:** 2025-10-11
**Versiya:** 1.0
**Status:** ✅ Production ready
