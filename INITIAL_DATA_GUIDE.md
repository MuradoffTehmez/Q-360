# Q360 İlkin Data Yükləmə Təlimatı

## 🎯 Ümumi Baxış

Q360 Performance Management sistemi üçün əhatəli demo və test dataları hazırlanmışdır. Bu data setində 10 istifadəçi, 2 təşkilat, 6 departament və bütün modullar üçün nümunə məlumatlar mövcuddur.

## 📦 Fixtures Tərkibi

### 1. Organizations & Departments (01_departments.json)
- **2 Təşkilat**:
  - Rəqəmsal İnkişaf və Nəqliyyat Nazirliyi (RİNN)
  - İqtisadiyyat Nazirliyi (İN)
- **6 Departament** (MPTT hierarkiyası)
- **12 Vəzifə** (müxtəlif səviyyələrdə)

### 2. Users & Profiles (02_accounts.json)
- **10 İstifadəçi** (tam profil məlumatları ilə)
- **Rollar**: superadmin (1), admin (2), manager (2), employee (5)
- **Departamentlər arası paylanma**

### 3. Competencies (03_competencies.json)
- **4 Bacarıq Səviyyəsi** (Əsas, Orta, Təkmil, Ekspert)
- **15 Kompetensiya** (Liderlik, Texniki, Soft Skills)
- **20 Vəzifə-Kompetensiya Əlaqəsi**
- **13 İstifadəçi Bacarığı** (təsdiqlənmiş)

### 4. Evaluations (04_evaluations.json)
- **5 Sual Kateqoriyası**
- **17 Qiymətləndirmə Sualı**
- **2 Kampaniya** (completed və active)

### 5. Training Resources (05_training.json)
- **12 Təlim Resursu**:
  - Kurslar (Python, Django, React, UI/UX)
  - Sertifikatlar (CISSP, CEH, PMP, PHR)
  - Workshop-lar (Liderlik, Ünsiyyət)
- **8 İstifadəçi Təlimi** (müxtəlif statuslarda)

### 6. Development Plans (06_development_plans.json)
- **6 İnkişaf Məqsədi** (active və pending)
- **6 Proqres Qeydi**

### 7. Workforce Planning (07_workforce_planning.json)
- **7 Talent Matrix Qiymətləndirməsi** (9-box model)
- **3 Kritik Rol** (succession planning)
- **3 Succession Candidate**
- **5 Kompetensiya Gap Təhlili**

### 8. Continuous Feedback (08_continuous_feedback.json)
- **6 Feedback Tag**
- **8 Tez Rəy** (recognition və improvement)
- **5 Feedback Bank**
- **5 İctimai Təqdir**

### 9. Support System (09_support.json)
- **5 Dəstək Sorğusu** (müxtəlif statuslarda)
- **8 Şərh**

## 🚀 Yükləmə Proseduru

### Addım 1: Database-i Hazırlayın

```bash
# Əvvəlcə migrate əmin olun ki, bütün modellər yaradılıb
python manage.py makemigrations
python manage.py migrate
```

### Addım 2: İlkin Dataları Yükləyin

**Ən asan yol** (tövsiyə edilir):
```bash
python manage.py load_initial_data
```

Bu command avtomatik olaraq bütün fixture-ləri düzgün ardıcıllıqla yükləyəcək.

### Alternativ: İstifadəçiləri atlayın

Əgər artıq istifadəçilər yaradılıbsa:
```bash
python manage.py load_initial_data --skip-users
```

### Alternativ: Manual yükləmə

```bash
python manage.py loaddata fixtures/01_departments.json
python manage.py loaddata fixtures/02_accounts.json
python manage.py loaddata fixtures/03_competencies.json
python manage.py loaddata fixtures/04_evaluations.json
python manage.py loaddata fixtures/05_training.json
python manage.py loaddata fixtures/06_development_plans.json
python manage.py loaddata fixtures/07_workforce_planning.json
python manage.py loaddata fixtures/08_continuous_feedback.json
python manage.py loaddata fixtures/09_support.json
```

## 👥 Test İstifadəçiləri

| Username | Parol | Rol | Departament | Vəzifə |
|----------|-------|-----|-------------|--------|
| admin | password | superadmin | - | Sistem Administrator |
| rashad.mammadov | password | admin | Rəqəmsal İnkişaf | Departament direktoru |
| leyla.huseynova | password | manager | E-xidmətlər | Şöbə müdiri |
| murad.aliyev | password | employee | E-xidmətlər | Baş mütəxəssis |
| nigar.hasanova | password | employee | E-xidmətlər | Aparıcı mütəxəssis |
| elvin.quliyev | password | employee | E-xidmətlər | Mütəxəssis |
| farid.ismayilov | password | manager | Kibertəhlükəsizlik | Şöbə müdiri |
| aysel.memmedova | password | employee | Kibertəhlükəsizlik | Kibertəhlükəsizlik mütəxəssisi |
| kamran.bashirov | password | admin | İnsan Resursları | HR Direktoru |
| sevinc.huseynli | password | employee | İnsan Resursları | HR Business Partner |

**⚠️ TƏHLÜKƏSİZLİK QEYDI**: Bu parollar yalnız demo və test üçündür. İstehsal mühitində dərhal dəyişdirilməlidir!

## 🧪 Test Ssenariləri

### 1. Qiymətləndirmə Sistemi
- **Admin** (kamran.bashirov) olaraq daxil olun
- Yeni qiymətləndirmə kampaniyası yaradın
- **Manager** (leyla.huseynova) olaraq daxil olub öz komandanızı qiymətləndirin

### 2. Təlim İdarəetməsi
- **Employee** (elvin.quliyev) olaraq təlim kataloquna baxın
- Təlimə yazılın
- Proqresi yeniləyin

### 3. İnkişaf Planları
- **Employee** (murad.aliyev) olaraq inkişaf məqsədi yaradın
- Proqres log əlavə edin
- **Manager** kimi təsdiqləyin

### 4. Kadr Planlaması
- **Admin** (kamran.bashirov) olaraq Talent Matrix-ə baxın
- 9-box categorization-u yoxlayın
- Succession planning məlumatlarını araşdırın
- Kompetensiya gap-ləri analiz edin

### 5. Davamlı Rəy
- **Employee** (nigar.hasanova) olaraq həmkarınıza feedback göndərin
- İctimai təqdir feed-ini yoxlayın
- Feedback bank statistikalarına baxın

### 6. Dəstək Sistemi
- **Employee** olaraq dəstək sorğusu yaradın
- **Admin** (admin) olaraq sorğuya cavab verin

## 🔧 Troubleshooting

### Problem: Duplicate key error

**Səbəb**: Database-də artıq data var

**Həll**:
```bash
# Database-i təmizləyin
python manage.py flush --no-input

# Və ya tamamilə yenidən yaradın
python manage.py migrate accounts zero
python manage.py migrate departments zero
python manage.py migrate competencies zero
python manage.py migrate evaluations zero
python manage.py migrate training zero
python manage.py migrate development_plans zero
python manage.py migrate workforce_planning zero
python manage.py migrate continuous_feedback zero
python manage.py migrate support zero

# Sonra yenidən migrate edin
python manage.py migrate
python manage.py load_initial_data
```

### Problem: Foreign key constraint error

**Səbəb**: Fixtures yanlış ardıcıllıqla yüklənib

**Həll**:
```bash
# Management command istifadə edin (avtomatik düzgün ardıcıllıq)
python manage.py load_initial_data
```

### Problem: File not found error

**Səbəb**: Fixtures qovluğunun yolu səhvdir

**Həll**:
```bash
# Fixtures qovluğunun olduğunu yoxlayın
ls fixtures/

# Və ya tam yol istifadə edin
python manage.py loaddata /full/path/to/fixtures/01_departments.json
```

### Problem: Password authentication failed

**Səbəb**: Password hash-lər düzgün deyil

**Həll**:
```bash
# Superuser yaradın
python manage.py createsuperuser

# Və ya passwordu reset edin
python manage.py changepassword admin
```

## 📊 Data Statistikaları

- **İstifadəçilər**: 10
- **Təşkilatlar**: 2
- **Departamentlər**: 6
- **Vəzifələr**: 12
- **Kompetensiyalar**: 15
- **Qiymətləndirmə Sualları**: 17
- **Təlim Resursları**: 12
- **İnkişaf Məqsədləri**: 6
- **Talent Assessments**: 7
- **Feedback-lər**: 8
- **Dəstək Sorğuları**: 5

## 📝 Qeydlər

1. **MPTT Support**: Department hierarchyası MPTT (Modified Preorder Tree Traversal) istifadə edir
2. **Simple History**: Bütün əsas modellər üçün tarixçə saxlanılır
3. **Real Data**: Azərbaycan dövlət strukturları əsasında simulyasiya edilmiş realistik data
4. **Fictiv Məlumat**: Bütün şəxsi məlumatlar fictivdir, real şəxslər deyil

## 🎓 Növbəti Addımlar

1. ✅ İlkin dataları yükləyin
2. ✅ Test istifadəçiləri ilə login olun
3. ✅ Hər bir modulu test edin
4. ✅ Demo ssenariləri keçin
5. ✅ Öz datanızı əlavə edin
6. ✅ Production üçün parolları dəyişdirin

## 📞 Dəstək

Əgər problem yaşasanız və ya sualınız olarsa:
- GitHub Issues açın
- Dokumentasiyaya baxın
- Development komandası ilə əlaqə saxlayın

---

**Uğurlar! 🚀**
