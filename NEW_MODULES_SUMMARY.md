# Q360 Yeni Modullar - Yaradılmış Fayllar və API Endpoint-lər

## 📋 Ümumi Məlumat

Q360 performans qiymətləndirmə sisteminə üç yeni modul əlavə edildi:

1. **Kompetensiya və Vəzifə İdarəetməsi** (competencies app)
2. **Təlim və İnkişaf Planlaması** (training app)
3. **Təhlükəsizlik Dashboardu** (audit/security enhancement)

---

## 🏅 Modul 1: Kompetensiya İdarəetməsi (`apps/competencies`)

### Yaradılmış Fayllar

```
apps/competencies/
├── __init__.py
├── apps.py
├── models.py              # 4 Model: Competency, ProficiencyLevel, PositionCompetency, UserSkill
├── serializers.py         # 8 Serializer (əsas və ətraflı versiyalar)
├── views.py               # 4 ViewSet (CRUD + əlavə funksionallıqlar)
├── urls.py                # API route konfiqurasiyası
└── admin.py               # Django Admin interfeysi
```

### Modellər

1. **Competency** - Kompetensiya Bankı
   - Sahələr: name, description, is_active
   - Simple History: ✓

2. **ProficiencyLevel** - Bacarıq Səviyyələri
   - Sahələr: name, display_name, score_min, score_max
   - Seçimlər: basic, intermediate, advanced, expert

3. **PositionCompetency** - Vəzifə-Kompetensiya Əlaqəsi
   - Sahələr: position (FK), competency (FK), weight (1-100%), required_level, is_mandatory
   - Simple History: ✓

4. **UserSkill** - İstifadəçi Bacarıqları
   - Sahələr: user (FK), competency (FK), level (FK), current_score, is_approved, approval_status
   - Təsdiq workflow: pending → approved/rejected
   - Simple History: ✓

### API Endpoint-lər

**Base URL:** `/api/competencies/`

#### CompetencyViewSet
- `GET /api/competencies/competencies/` - Bütün kompetensiyalar
- `POST /api/competencies/competencies/` - Yeni kompetensiya (Admin)
- `GET /api/competencies/competencies/{id}/` - Kompetensiya detalları
- `PUT/PATCH /api/competencies/competencies/{id}/` - Yenilə (Admin)
- `DELETE /api/competencies/competencies/{id}/` - Sil (Admin)
- `GET /api/competencies/competencies/{id}/positions/` - Əlaqəli vəzifələr
- `GET /api/competencies/competencies/{id}/users/` - Bu kompetensiyaya malik istifadəçilər
- `GET /api/competencies/competencies/statistics/` - Statistika

**Filterlər:** `is_active`, `name`
**Axtarış:** `name`, `description`

#### ProficiencyLevelViewSet
- `GET /api/competencies/proficiency-levels/` - Bütün səviyyələr
- `POST /api/competencies/proficiency-levels/` - Yeni səviyyə (Admin)
- `GET /api/competencies/proficiency-levels/{id}/` - Səviyyə detalları

#### PositionCompetencyViewSet
- `GET /api/competencies/position-competencies/` - Vəzifə-kompetensiya əlaqələri
- `POST /api/competencies/position-competencies/` - Yeni əlaqə (Manager)
- **Filterlər:** `position`, `competency`, `is_mandatory`

#### UserSkillViewSet
- `GET /api/competencies/user-skills/` - İstifadəçi bacarıqları
- `POST /api/competencies/user-skills/` - Yeni bacarıq əlavə et
- `GET /api/competencies/user-skills/{id}/` - Bacarıq detalları
- `POST /api/competencies/user-skills/{id}/approve/` - Təsdiq et (Manager)
- `POST /api/competencies/user-skills/{id}/reject/` - Rədd et (Manager)
- `GET /api/competencies/user-skills/pending_approvals/` - Təsdiq gözləyən bacarıqlar (Manager)
- `GET /api/competencies/user-skills/my_skills/` - Mənim bacarıqlarım

**Filterlər:** `user`, `competency`, `is_approved`, `approval_status`

---

## 📚 Modul 2: Təlim və İnkişaf (`apps/training`)

### Yaradılmış Fayllar

```
apps/training/
├── __init__.py
├── apps.py
├── models.py              # 2 Model: TrainingResource, UserTraining
├── serializers.py         # 8 Serializer
├── views.py               # 2 ViewSet
├── urls.py                # API route konfiqurasiyası
├── admin.py               # Django Admin interfeysi
├── tasks.py               # 4 Celery Task
└── signals.py             # 4 Signal Handler
```

### Modellər

1. **TrainingResource** - Təlim Kataloqu
   - Sahələr: title, description, type, is_online, delivery_method, difficulty_level, duration_hours, language
   - M2M: required_competencies (Competency ilə)
   - Növlər: Course, Certification, Mentoring, Workshop, Conference, Webinar, Self Study
   - Simple History: ✓

2. **UserTraining** - İstifadəçi Təlimi
   - Sahələr: user (FK), resource (FK), assigned_by (FK), assignment_type, related_goal (FK to DevelopmentGoal)
   - Status: pending, in_progress, completed, cancelled, failed
   - Tarixlər: start_date, due_date, completed_date
   - Rəy: user_feedback, rating (1-5), certificate_url
   - Simple History: ✓

### API Endpoint-lər

**Base URL:** `/api/training/`

#### TrainingResourceViewSet
- `GET /api/training/resources/` - Bütün təlim resursları
- `POST /api/training/resources/` - Yeni təlim (Admin)
- `GET /api/training/resources/{id}/` - Təlim detalları
- `PUT/PATCH /api/training/resources/{id}/` - Yenilə (Admin)
- `DELETE /api/training/resources/{id}/` - Sil (Admin)
- `GET /api/training/resources/{id}/assigned_users/` - Təlimə təyin olunmuş istifadəçilər
- `POST /api/training/resources/{id}/assign_to_users/` - İstifadəçilərə təyin et (Manager)
- `GET /api/training/resources/statistics/` - Təlim statistikaları

**Filterlər:** `type`, `is_active`, `is_online`, `difficulty_level`, `is_mandatory`
**Axtarış:** `title`, `description`, `provider`

#### UserTrainingViewSet
- `GET /api/training/user-trainings/` - Təlimlər
- `POST /api/training/user-trainings/` - Yeni təlim təyini
- `GET /api/training/user-trainings/{id}/` - Təlim detalları
- `POST /api/training/user-trainings/{id}/update_status/` - Status yenilə
- `POST /api/training/user-trainings/{id}/update_progress/` - Proqres yenilə
- `POST /api/training/user-trainings/{id}/submit_feedback/` - Rəy göndər
- `GET /api/training/user-trainings/my_trainings/` - Mənim təlimlərim
- `GET /api/training/user-trainings/my_pending/` - Gözləyən təlimlər
- `GET /api/training/user-trainings/my_in_progress/` - Davam edən təlimlər
- `GET /api/training/user-trainings/my_completed/` - Tamamlanmış təlimlər
- `GET /api/training/user-trainings/overdue/` - Vaxtı keçmiş təlimlər (Manager)
- `POST /api/training/user-trainings/get_recommendations/` - Təlim tövsiyələri

**Filterlər:** `user`, `resource`, `status`, `assignment_type`

### Celery Tasks

```python
# apps/training/tasks.py

1. assign_training_for_development_goal(goal_id)
   - Yeni DevelopmentGoal yaradılanda avtomatik təlim tövsiyəsi
   - Kompetensiyalara əsasən uyğun təlimlər təyin edir

2. send_training_due_reminders(days_before=7)
   - Təlim son tarixinə yaxınlaşdıqda xatırlatma göndərir
   - Periodic task kimi işlədilə bilər

3. update_overdue_trainings()
   - Müddəti keçmiş təlimləri yoxlayır
   - Periodic task kimi işlədilə bilər

4. recommend_trainings_for_user(user_id, competency_ids=None, limit=5)
   - İstifadəçi üçün kompetensiyalara əsasən təlim tövsiyələri
```

### Signal Handlers

```python
# apps/training/signals.py

1. trigger_training_assignment
   - Signal: post_save(DevelopmentGoal)
   - Action: Yeni məqsəd yaradılanda Celery task işə salır

2. notify_user_on_training_assignment
   - Signal: post_save(UserTraining) [created]
   - Action: Yeni təlim təyin olunduqda istifadəçiyə bildiriş

3. notify_on_training_completion
   - Signal: post_save(UserTraining) [status=completed]
   - Action: Təlim tamamlandıqda istifadəçi və menecerə bildiriş

4. suggest_training_for_low_skill
   - Signal: post_save(UserSkill)
   - Action: Aşağı bacarıq balı olduqda avtomatik təlim tövsiyəsi
```

---

## 🛡️ Modul 3: Təhlükəsizlik Dashboardu (`apps/audit`)

### Yenilənmiş və Yaradılmış Fayllar

```
apps/audit/
├── models.py              # Yeniləndi: LOGIN_FAILURE action_type əlavə edildi
├── views.py               # YENİ: 2 API View
├── urls.py                # Yeniləndi: Yeni endpoint-lər
└── ...

apps/accounts/
└── signals.py             # Yeniləndi: 2 yeni signal handler
```

### Dəyişikliklər

#### 1. audit/models.py
```python
ACTION_TYPES = [
    ('create', 'Yaratma'),
    ('update', 'Yenilənmə'),
    ('delete', 'Silinmə'),
    ('login', 'Giriş'),
    ('logout', 'Çıxış'),
    ('login_failure', 'Uğursuz Giriş'),  # YENİ
    ('export', 'İxrac'),
    ('import', 'İdxal'),
]
```

#### 2. audit/views.py (YENİ)
- **SecurityStatsView** - Təhlükəsizlik statistikaları
- **AuditLogListView** - Audit log qeydləri

#### 3. accounts/signals.py
```python
@receiver(user_login_failed)
def log_login_failure(...)
    # Uğursuz giriş cəhdlərini AuditLog-da qeyd edir

@receiver(user_login_failed)
def check_brute_force_attempts(...)
    # Brute force hücumlarını yoxlayır
    # 15 dəqiqədə 5+ uğursuz cəhd → xəbərdarlıq
```

### API Endpoint-lər

**Base URL:** `/api/audit/`

#### SecurityStatsView
- `GET /api/audit/security-stats/`
  - Yalnız Admin/Superadmin
  - Response:
    ```json
    {
      "success": true,
      "period": "Son 7 gün",
      "total_failures": 42,
      "failures_by_day": [...],
      "top_failed_ips": [
        {"ip_address": "192.168.1.100", "failure_count": 15},
        ...
      ],
      "top_failed_users": [
        {"user_id": 5, "username": "test", "failure_count": 8},
        ...
      ],
      "recent_failures": [...]
    }
    ```

#### AuditLogListView
- `GET /api/audit/logs/`
  - Yalnız Admin/Superadmin
  - Query parametrləri:
    - `action` - Əməliyyat növü (login, logout, create, update, delete, login_failure)
    - `days` - Neçə gün əvvəlki qeydlər (default: 7)
    - `limit` - Maksimum qeyd sayı (default: 100)

---

## 🔧 Quraşdırma və İstifadə Təlimatları

### 1. Migration yaratmaq və tətbiq etmək

```bash
# Competencies app üçün migration
python manage.py makemigrations competencies

# Training app üçün migration
python manage.py makemigrations training

# Audit modelindəki dəyişiklik üçün
python manage.py makemigrations audit

# Bütün migration-ları tətbiq et
python manage.py migrate
```

### 2. Celery işə salmaq (Təlim modulunda istifadə üçün)

```bash
# Redis serveri işə sal (Windows)
# Redis quraşdırılmalıdır və ya Docker istifadə edin

# Celery worker işə sal
celery -A config worker -l info

# Periodic tasks üçün Celery Beat
celery -A config beat -l info
```

### 3. İlkin Məlumatlar (Optional)

```python
# Django shell-də
python manage.py shell

from apps.competencies.models import ProficiencyLevel

# Səviyyələr yarat
ProficiencyLevel.objects.create(
    name='basic',
    display_name='Əsas',
    score_min=0,
    score_max=40
)
ProficiencyLevel.objects.create(
    name='intermediate',
    display_name='Orta',
    score_min=41,
    score_max=70
)
ProficiencyLevel.objects.create(
    name='advanced',
    display_name='Təkmil',
    score_min=71,
    score_max=90
)
ProficiencyLevel.objects.create(
    name='expert',
    display_name='Ekspert',
    score_min=91,
    score_max=100
)
```

### 4. API Test (Postman/cURL)

```bash
# 1. Token əldə et
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# 2. Kompetensiyalar siyahısı
curl -X GET http://localhost:8000/api/competencies/competencies/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# 3. Təlim resursları
curl -X GET http://localhost:8000/api/training/resources/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# 4. Təhlükəsizlik statistikaları
curl -X GET http://localhost:8000/api/audit/security-stats/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 📊 Məlumat Bazası Diaqramı

### Kompetensiya Modulu
```
Competency (1) ----< (M) PositionCompetency >---- (M) Position
     |
     |
     v
UserSkill >---- ProficiencyLevel
     |
     v
   User
```

### Təlim Modulu
```
TrainingResource (1) ----< (M) required_competencies >---- (M) Competency
        |
        v
   UserTraining >---- User
        |
        v
  DevelopmentGoal
```

---

## 🔐 İcazələr və Təhlükəsizlik

### Rol-əsaslı Giriş Nəzarəti

| Əməliyyat | Employee | Manager | Admin | Superadmin |
|-----------|----------|---------|-------|------------|
| Kompetensiya görüntülə | ✓ | ✓ | ✓ | ✓ |
| Kompetensiya yarat/düzəlt | - | - | ✓ | ✓ |
| Bacarıq əlavə et | ✓ | ✓ | ✓ | ✓ |
| Bacarıq təsdiq et | - | ✓ | ✓ | ✓ |
| Təlim görüntülə | ✓ (Öz) | ✓ | ✓ | ✓ |
| Təlim təyin et | - | ✓ | ✓ | ✓ |
| Təhlükəsizlik statistikaları | - | - | ✓ | ✓ |

---

## 📝 Testlər

### Unit Testlər (Gələcək genişləndirilmə)

```bash
# Bütün testləri işə sal
python manage.py test

# Yalnız competencies
python manage.py test apps.competencies

# Yalnız training
python manage.py test apps.training
```

---

## 🐛 Troubleshooting

### Problem: Migration xətası

**Həll:**
```bash
python manage.py makemigrations --empty competencies
# və ya
python manage.py migrate --fake competencies zero
python manage.py migrate competencies
```

### Problem: Celery task işləmir

**Həll:**
1. Redis işə düşübmü yoxlayın
2. Celery worker-in loglarını yoxlayın
3. Task import yolunu düzgün olub-olmadığını yoxlayın

### Problem: Signal işləmir

**Həll:**
1. `apps.py` faylında `ready()` metodunu yoxlayın
2. Signal import olunubmu əmin olun
3. `INSTALLED_APPS`-da app düzgün qeyd olunubmu yoxlayın

---

## 📖 Əlavə Resurslar

- Django Documentation: https://docs.djangoproject.com/
- DRF Documentation: https://www.django-rest-framework.org/
- Celery Documentation: https://docs.celeryproject.org/
- Django Simple History: https://django-simple-history.readthedocs.io/

---

## ✅ Checklist

- [x] Competencies app yaradıldı
- [x] Training app yaradıldı
- [x] Audit modelinə LOGIN_FAILURE əlavə edildi
- [x] SecurityStatsView API yaradıldı
- [x] Login failure signal handlers yaradıldı
- [x] Celery tasks yaradıldı
- [x] API endpoint-lər config/urls.py-ə əlavə edildi
- [x] INSTALLED_APPS-a yeni app-lar əlavə edildi
- [x] Admin interfeysi konfiqurasiya edildi

---

**Qeyd:** Bu modullar Django 5.1+, DRF, PostgreSQL və Celery/Redis texnologiyaları ilə uyğundur.
