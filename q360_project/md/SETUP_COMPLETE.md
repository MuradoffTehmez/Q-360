# ✅ Q360 İlkin Data Yükləndi!

## 🎉 Uğurla Tamamlandı

İlkin demo dataları uğurla database-ə yükləndi!

## 📊 Yüklənmiş Data

- ✅ **Təşkilatlar**: 3
- ✅ **Departamentlər**: 9
- ✅ **İstifadəçilər**: 23
- ✅ **Kompetensiyalar**: 11
- ✅ **Səviyyələr**: 2
- ✅ **Təlim Resursları**: 1+
- ✅ **İnkişaf Məqsədləri**: 1+

## 🔐 Giriş Məlumatları

### Test İstifadəçiləri

| İstifadəçi Adı | Parol | Rol | Təsvir |
|----------------|-------|-----|---------|
| `admin` | `password` | Superadmin | Sistem administratoru |
| `rashad.mammadov` | `password` | Admin | Departament direktoru |
| `leyla.huseynova` | `password` | Manager | Şöbə müdiri |
| `murad.aliyev` | `password` | Employee | Baş mütəxəssis |

**⚠️ TƏHLÜKƏSİZLİK QEYDI**: Bu parollar demo üçündür. İstehsal mühitində dərhal dəyişdirin!

## 🚀 Sistemi İşə Salın

### 1. Development Server

```bash
cd q360_project
python manage.py runserver
```

Sonra brauzerə keçin: **http://localhost:8000**

### 2. Admin Panel

Admin panel-ə daxil olun: **http://localhost:8000/admin/**

- **İstifadəçi**: `admin`
- **Parol**: `password`

### 3. API Endpoints

API-ləri test edin:
- **http://localhost:8000/api/** - API root
- **http://localhost:8000/api/swagger/** - Swagger dokumentasiyası
- **http://localhost:8000/api/redoc/** - ReDoc dokumentasiyası

## 🧪 Test Ssenariləri

### Ssenariya 1: İstifadəçi İdarəetməsi
1. Admin panel-ə daxil olun
2. Users bölməsinə keçin
3. Yeni istifadəçi əlavə edin
4. Departament və rol təyin edin

### Ssenariya 2: Kompetensiya İdarəetməsi
1. `leyla.huseynova` olaraq daxil olun
2. Competencies bölməsinə keçin
3. İstifadəçilərin bacarıqlarını göstərin
4. Yeni bacarıq əlavə edin və təsdiqləyin

### Ssenariya 3: Təlim Təyin Etmə
1. Manager olaraq daxil olun
2. Training Resources-ə baxın
3. İşçiyə təlim təyin edin
4. Proqresi izləyin

### Ssenariya 4: İnkişaf Planları
1. Employee olaraq daxil olun
2. Development Goals yaradın
3. Proqres log əlavə edin
4. Manager təsdiqini gözləyin

## ⚙️ Əlavə Konfiqurasiyalar

### Redis və Celery (Optional)

Əgər background tasks istifadə etmək istəyirsinizsə:

```bash
# Redis yüklə və işə sal (Windows)
# https://redis.io/download

# Ayrı terminal-da Celery işçisini başlat
celery -A config worker -l info

# Celery beat başlat (scheduled tasks üçün)
celery -A config beat -l info
```

### Email Konfiqurasiyası

`config/settings.py` faylında email settings-i yeniləyin:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 📚 Əlavə Data Yükləmək

Daha çox demo data lazımdırsa:

### Tam İstifadəçi Dəsti

```bash
python manage.py create_demo_users
```

Bu command 10 istifadəçi yaradacaq (düzgün hash-lənmiş parollarla).

### Xüsusi Modullar

Hər modul üçün xüsusi data yükləmək istəyirsinizsə, fixture fayllarını işə salın:

```bash
# Qiymətləndirmə dataları
python manage.py loaddata fixtures/04_evaluations.json

# Təlim dataları
python manage.py loaddata fixtures/05_training.json

# Workforce planning
python manage.py loaddata fixtures/07_workforce_planning.json
```

**QEYD**: Fixture-lər `auto_now_add` field problemi səbəbindən işə düşməyə bilər.
Əvəzinə `load_all_initial_data` command-ı istifadə edin.

## 🐛 Problemlər və Həllər

### Problem: "Connection to Redis lost"

**Həll**: Redis işləmir. İki seçim:
1. Redis quraşdırın və işə salın (background tasks üçün)
2. İgnore edin (optional feature-dir)

### Problem: Fixture yükləmə xətası

**Həll**: `load_all_initial_data` command-ı istifadə edin (JSON fixtures əvəzinə):

```bash
python manage.py load_all_initial_data
```

### Problem: Parol düzgün deyil

**Həll**: Parolu sıfırlayın:

```bash
python manage.py changepassword admin
```

Və ya yeni superuser yaradın:

```bash
python manage.py createsuperuser
```

## 📖 Dokumentasiya

Ətraflı məlumat üçün:

- **fixtures/README.md** - Fixture-lər haqqında
- **INITIAL_DATA_GUIDE.md** - Ətraflı yükləmə təlimatı
- **docs/** qovluğu - API və modul dokumentasiyası

## 🎓 Növbəti Addımlar

1. ✅ Sistemi test edin və mövcud dataları araşdırın
2. ✅ Öz təşkilatınızın strukturunu yaradın
3. ✅ Real istifadəçiləri əlavə edin
4. ✅ Kompetensiya modelinizi konfiqurasiya edin
5. ✅ İlk qiymətləndirmə kampaniyasını başladın
6. ✅ Production üçün hazırlayın

## 💡 Məsləhətlər

- **Admin Panel-dən başlayın**: Məlumatları görmək və redaktə etmək ən asan yol
- **API Documentation-a baxın**: Swagger/ReDoc ilə API-ləri kəşf edin
- **Test Data-nı silin**: Real data əlavə etməzdən əvvəl demo dataları silin
- **Backup alın**: Dəyişiklik etməzdən əvvəl həmişə backup alın

## 🆘 Dəstək

Problem yaşayırsınız?

1. **Log-lara baxın**: Terminal output-a diqqət edin
2. **Database-i yoxlayın**: Admin panel-dən data-nı göstərin
3. **Documentation oxuyun**: Çox sualın cavabı orada var
4. **GitHub Issues**: Bug report və feature request üçün

---

**Uğurlar! 🚀 Q360 sistemi istifadəyə hazırdır!**

*Demo data ilə: ✓ Təşkilatlar ✓ İstifadəçilər ✓ Kompetensiyalar ✓ Təlimlər və daha çox!*
