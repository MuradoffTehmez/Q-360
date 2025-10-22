# Q360 Performance Evaluation System - Yeni Modullar

## 🎯 Layihə Haqqında

Q360 Performance Evaluation System üçün 3 yeni modul əlavə edildi:
1. **Competencies & Skills Management** - Kompetensiya və bacarıq idarəetməsi
2. **Training & Development** - Təlim və inkişaf planlaşdırması
3. **Security Dashboard** - Təhlükəsizlik monitorinqi

---

## 📦 Yaradılmış Fayllar

### Backend (Django/Python)

#### Competencies App
```
apps/competencies/
├── models.py              # 4 model (Competency, ProficiencyLevel, PositionCompetency, UserSkill)
├── serializers.py         # 8 serializer
├── views.py               # 4 ViewSet
├── template_views.py      # 3 template view
├── urls.py                # URL konfiqurasiyası
├── admin.py               # Admin panel konfiqurasiyası
└── apps.py                # App konfiqurasiyası
```

#### Training App
```
apps/training/
├── models.py              # 2 model (TrainingResource, UserTraining)
├── serializers.py         # 8 serializer
├── views.py               # 2 ViewSet
├── template_views.py      # 3 template view
├── tasks.py               # 4 Celery task
├── signals.py             # 4 signal handler
├── urls.py                # URL konfiqurasiyası
├── admin.py               # Admin panel konfiqurasiyası
└── apps.py                # App konfiqurasiyası
```

#### Audit App (Updated)
```
apps/audit/
├── models.py              # AuditLog (LOGIN_FAILURE əlavə edildi)
├── views.py               # SecurityStatsView, AuditLogListView
├── template_views.py      # Security dashboard view
└── urls.py                # URL konfiqurasiyası

apps/accounts/
└── signals.py             # Login failure tracking və brute force detection
```

### Frontend (HTML/CSS/JavaScript)

```
templates/
├── competencies/
│   ├── competency_list.html      # Kompetensiya siyahısı (AJAX, filter, CRUD)
│   ├── competency_detail.html    # Kompetensiya detayları (Chart.js)
│   └── my_skills.html            # İstifadəçi bacarıqları
├── training/
│   ├── my_trainings.html         # Mənim təlimlərim (tab-based)
│   ├── catalog.html              # Təlim kataloqu (filter)
│   └── training_detail.html      # Təlim detayları
└── audit/
    └── security_dashboard.html   # Təhlükəsizlik dashboard (Chart.js)
```

### Konfiqurasiya

```
config/
├── settings.py            # INSTALLED_APPS yeniləndi
└── urls.py                # Yeni URL-lər əlavə edildi

templates/base/
└── sidebar.html           # Navigation menu yeniləndi
```

### Dokumentasiya

```
📄 NEW_MODULES_SUMMARY.md      # Backend texniki dokumentasiya
📄 HTML_TEMPLATES_README.md    # Frontend istifadə təlimatı
📄 IMPLEMENTATION_STATUS.md    # İmplementasiya statusu
📄 DEPLOYMENT_GUIDE.md         # Deployment təlimatları
📄 README_YENI_MODULLAR.md     # Bu fayl (ümumi bələdçi)
```

---

## 🚀 Sürətli Başlanğıc

### 1. Migration-lar

```bash
python manage.py makemigrations competencies training audit
python manage.py migrate
```

### 2. İlkin Məlumatlar

```bash
python manage.py shell
```

```python
from apps.competencies.models import ProficiencyLevel

ProficiencyLevel.objects.create(name='basic', score_min=0, score_max=25)
ProficiencyLevel.objects.create(name='intermediate', score_min=26, score_max=50)
ProficiencyLevel.objects.create(name='advanced', score_min=51, score_max=75)
ProficiencyLevel.objects.create(name='expert', score_min=76, score_max=100)
exit()
```

### 3. Redis və Celery

```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Celery Worker
celery -A config worker -l info --pool=solo

# Terminal 3: Django
python manage.py runserver
```

### 4. Səhifələrə Get

```
http://localhost:8000/competencies/
http://localhost:8000/training/
http://localhost:8000/audit/security/  (Admin only)
```

---

## 📚 Ətraflı Dokumentasiya

| Sənəd | Məzmun |
|-------|--------|
| `NEW_MODULES_SUMMARY.md` | Backend modellər, API-lər, Celery task-lar |
| `HTML_TEMPLATES_README.md` | Frontend səhifələr, URL-lər, JavaScript |
| `DEPLOYMENT_GUIDE.md` | Addım-addım deployment təlimatı |
| `IMPLEMENTATION_STATUS.md` | Tamamlanmış işlər və statistika |

---

## 🔑 Əsas Xüsusiyyətlər

### Competencies Modulu

✅ **Kompetensiya İdarəetməsi**
- Kompetensiya yaratma, oxuma, yeniləmə, silmə (CRUD)
- Pozisiya-kompetensiya əlaqələri
- Çəki (weight) sistemi

✅ **Bacarıq İdarəetməsi**
- İstifadəçi bacarıqlarının qeydiyyatı
- Təsdiq prosesi (pending → approved/rejected)
- 4 səviyyəli proficiency sistemi (basic → expert)
- Self-assessment balları (0-100)

✅ **Statistika və Reporting**
- Real-time statistika kartları
- Bacarıq səviyyəsi paylanması (Chart.js)
- İstifadəçi və pozisiya sayları

### Training Modulu

✅ **Təlim Resurs Kataloqu**
- 4 növ təlim (course, certification, mentoring, workshop)
- 3 çətinlik səviyyəsi (beginner, intermediate, advanced)
- Xarici linklər və material yükləmə
- Qiymət və müddət məlumatları

✅ **İstifadəçi Təlimləri**
- Təlim təyinatı və izləmə
- Progress tracking (0-100%)
- 4 status (pending, in_progress, completed, cancelled)
- Son tarix (due date) idarəetməsi
- Notes və sertifikat qeydləri

✅ **Avtomatlaşdırma (Celery)**
- Development goal-a görə avtomatik təlim təyinatı
- Son tarix xatırlatmaları
- Kompetensiya boşluqlarına görə təlim tövsiyələri
- Təlim tamamlama bildirişləri

### Security Modulu

✅ **Login Failure Tracking**
- Uğursuz giriş cəhdlərinin qeydiyyatı
- IP ünvanı və user agent məlumatları
- Timestamp və istifadəçi məlumatları

✅ **Brute Force Detection**
- 15 dəqiqə ərzində 5+ uğursuz cəhd aşkarlanması
- Superadmin-lərə avtomatik xəbərdarlıq
- Django signals ilə real-time monitoring

✅ **Security Dashboard**
- Son 7 günün statistikası
- Chart.js ilə vizual qrafiklər
- Top 3 şübhəli IP ünvanları
- Top 3 problem istifadəçilər
- Son uğursuz cəhdlərin siyahısı

---

## 🔗 URL Strukturu

### Template URLs (İstifadəçi İnterfeysi)

```
Competencies:
/competencies/                  → Siyahı
/competencies/<id>/             → Detaylar
/competencies/my-skills/        → Mənim bacarıqlarım
/competencies/manage/           → İdarəetmə (Admin)

Training:
/training/                      → Mənim təlimlərim
/training/<id>/                 → Təlim detayları
/training/catalog/              → Katalog
/training/manage/               → İdarəetmə (Admin/Manager)

Security:
/audit/security/                → Dashboard (Admin only)
```

### API URLs (AJAX və Mobil)

```
Competencies API:
/api/competencies/api/competencies/              → GET/POST/PUT/DELETE
/api/competencies/api/competencies/statistics/   → GET statistics
/api/competencies/api/user-skills/my_skills/     → GET my skills
/api/competencies/api/user-skills/{id}/approve/  → POST approve skill

Training API:
/api/training/api/resources/                     → GET/POST training resources
/api/training/api/user-trainings/my_pending/     → GET pending trainings
/api/training/api/user-trainings/my_in_progress/ → GET active trainings
/api/training/api/user-trainings/my_completed/   → GET completed trainings

Security API:
/api/audit/api/security-stats/                   → GET security statistics
/api/audit/api/logs/                             → GET audit logs
```

---

## 👥 İcazələr (Permissions)

| Funksionallıq | Employee | Manager | Admin |
|---------------|----------|---------|-------|
| **Competencies** ||||
| Siyahıya baxma | ✓ | ✓ | ✓ |
| Kompetensiya CRUD | ✗ | ✗ | ✓ |
| Öz bacarıqlarını əlavə etmə | ✓ | ✓ | ✓ |
| Bacarıq təsdiqi | ✗ | ✓ | ✓ |
| **Training** ||||
| Kataloqa baxma | ✓ | ✓ | ✓ |
| Öz təlimlərini görme | ✓ | ✓ | ✓ |
| Təlim təyin etmə | ✗ | ✓ | ✓ |
| Təlim CRUD | ✗ | ✗ | ✓ |
| **Security** ||||
| Dashboard baxışı | ✗ | ✗ | ✓ |
| Audit logs oxuma | ✗ | ✗ | ✓ |

---

## 🛠 Texnologiyalar

### Backend
- **Django 5.1+** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database
- **Celery** - Asynchronous task processing
- **Redis** - Message broker və cache
- **django-simple-history** - Audit trail
- **JWT** - Authentication

### Frontend
- **Bootstrap 5** - UI framework
- **jQuery** - AJAX və DOM manipulation
- **Chart.js** - Data visualization
- **Font Awesome** - Icons

---

## 📊 Statistika

- **Python Faylları:** 15+
- **HTML Səhifələri:** 7
- **Models:** 6 əsas model
- **API Endpoints:** 20+
- **Celery Tasks:** 4
- **Signal Handlers:** 6
- **JavaScript Functions:** 30+

---

## 🔄 Celery Tasks

| Task | Məqsəd | Schedule |
|------|--------|----------|
| `assign_training_for_development_goal` | Yeni hədəfə təlim təyin edir | On-demand (signal) |
| `send_training_due_reminders` | Son tarix xatırlatması göndərir | Daily (Celery Beat) |
| `recommend_trainings_for_user` | İstifadəçiyə təlim tövsiyə edir | On-demand |
| `update_user_skill_stats` | Bacarıq statistikalarını yeniləyir | Weekly (Celery Beat) |

---

## 🔔 Signal Handlers

### Training Signals
- `trigger_training_assignment` - Development goal yaradılanda
- `notify_training_assignment` - Təlim təyin edildikdə
- `suggest_training_for_low_skill` - Aşağı bacarıq balı olduqda
- `notify_training_completion` - Təlim tamamlandıqda

### Security Signals
- `log_login_failure` - Uğursuz giriş cəhdini qeyd edir
- `check_brute_force_attempts` - Brute force hücumunu aşkar edir

---

## 🎨 UI Komponentləri

- ✅ Responsive tables
- ✅ Modal dialogs
- ✅ Tab navigation
- ✅ Progress bars
- ✅ Card layouts
- ✅ Chart.js visualizations
- ✅ AJAX content loading
- ✅ Form validation
- ✅ Bootstrap badges
- ✅ Font Awesome icons

---

## 🧪 Test Ssenariləri

### 1. Bacarıq Əlavə Etmək
1. Login → My Skills
2. "Add Skill" button
3. Select competency & level
4. Submit form
5. Skill appears in list

### 2. Təlim Təyin Etmək (Manager)
1. Admin panel → User Trainings
2. Create new assignment
3. Select user & resource
4. Set due date
5. User receives notification

### 3. Təhlükəsizlik Monitorinqi (Admin)
1. Login as admin
2. Go to /audit/security/
3. View statistics & charts
4. Check suspicious IPs
5. Review recent failures

---

## 📞 Dəstək və Məsləhət

### Problem Həlli

1. **Migration Errors**
   ```bash
   python manage.py migrate --run-syncdb
   ```

2. **Celery Connection Error**
   - Redis işlədiyini yoxlayın: `redis-cli ping`
   - CELERY_BROKER_URL settings-də düzdür

3. **Static Files 404**
   ```bash
   python manage.py collectstatic
   ```

4. **API 403 Forbidden**
   - JWT token doğru göndərilir: `Authorization: Bearer TOKEN`

### Faydalı Komandalar

```bash
# Database reset (development only!)
python manage.py flush

# Create superuser
python manage.py createsuperuser

# Check for issues
python manage.py check

# View Celery registered tasks
celery -A config inspect registered

# Monitor Redis
redis-cli monitor
```

---

## 📖 Növbəti Addımlar

1. ✅ Migration-ları tətbiq edin
2. ✅ İlkin məlumatları yaradın
3. ✅ Celery/Redis işə salın
4. ✅ API-ları test edin
5. ✅ Frontend səhifələri yoxlayın
6. 🔄 Production-a deploy edin

---

## 📝 Qeydlər

- Bütün kod Python 3.8+ və Django 5.1+ uyğundur
- Frontend Bootstrap 5 və jQuery istifadə edir
- API-lər JWT authentication tələb edir
- Celery task-lar Redis broker istifadə edir
- Audit trail django-simple-history ilə təmin olunur

---

## 🏆 Nəticə

3 yeni modul tam funksional olaraq implementasiya edilib və istifadəyə hazırdır:

✅ **Competencies** - Kompetensiya və bacarıq idarəetməsi
✅ **Training** - Təlim planlaşdırma və izləmə
✅ **Security** - Təhlükəsizlik monitorinqi

**Yaradılma tarixi:** 2025-10-11
**Status:** ✅ Production Ready
**Versiya:** 1.0

---

**Müəllif:** Q360 Development Team
**Layihə:** Q360 Performance Evaluation System
