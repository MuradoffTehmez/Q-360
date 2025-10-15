# Q360 İlkin Data Fixtures

Bu qovluqda Q360 Performance Management sistemi üçün ilkin test və demo dataları yerləşir.

## Fixtures Siyahısı

1. **01_departments.json** - Təşkilatlar, Departamentlər və Vəzifələr
   - 2 təşkilat (RİNN, İN)
   - 6 departament (hierarkik struktur)
   - 12 vəzifə

2. **02_accounts.json** - İstifadəçilər və Profillər
   - 10 istifadəçi (admin, manager, employee rolları)
   - Tam profil məlumatları

3. **03_competencies.json** - Kompetensiyalar və Bacarıqlar
   - 4 bacarıq səviyyəsi (Əsas, Orta, Təkmil, Ekspert)
   - 15 kompetensiya
   - 20 vəzifə-kompetensiya əlaqəsi
   - 13 istifadəçi bacarığı

4. **04_evaluations.json** - Qiymətləndirmə Sistemi
   - 5 sual kateqoriyası
   - 17 qiymətləndirmə sualı
   - 2 qiymətləndirmə kampaniyası

5. **05_training.json** - Təlim Resursları
   - 12 təlim resursu (kurslar, sertifikatlar, workshop-lar)
   - 8 istifadəçi təlimi (müxtəlif statuslarda)

6. **06_development_plans.json** - İnkişaf Planları
   - 6 inkişaf məqsədi
   - 6 proqres qeydi

7. **07_workforce_planning.json** - Kadr Planlaması
   - 7 talent matrix qiymətləndirməsi (9-box)
   - 3 kritik rol
   - 3 succession candidate
   - 5 kompetensiya gap təhlili

8. **08_continuous_feedback.json** - Davamlı Rəy Sistemi
   - 6 feedback tag
   - 8 tez rəy
   - 5 feedback bank
   - 5 ictimai təqdir

9. **09_support.json** - Dəstək Sistemi
   - 5 dəstək sorğusu
   - 8 şərh

## İstifadə

### Bütün dataları yükləmək

```bash
python manage.py load_initial_data
```

### İstifadəçiləri atlamaq (artıq users varsa)

```bash
python manage.py load_initial_data --skip-users
```

### Ayrı-ayrı fixture yükləmək

```bash
python manage.py loaddata fixtures/01_departments.json
python manage.py loaddata fixtures/02_accounts.json
# və s.
```

## Test İstifadəçiləri

| İstifadəçi | Rol | Departament | Parol |
|------------|-----|-------------|-------|
| admin | superadmin | - | password |
| rashad.mammadov | admin | Rəqəmsal İnkişaf | password |
| leyla.huseynova | manager | E-xidmətlər | password |
| murad.aliyev | employee | E-xidmətlər | password |
| nigar.hasanova | employee | E-xidmətlər | password |
| elvin.quliyev | employee | E-xidmətlər | password |
| farid.ismayilov | manager | Kibertəhlükəsizlik | password |
| aysel.memmedova | employee | Kibertəhlükəsizlik | password |
| kamran.bashirov | admin | İnsan Resursları | password |
| sevinc.huseynli | employee | İnsan Resursları | password |

**QEYD:** İstehsal mühitində bu parollar dərhal dəyişdirilməlidir!

## Dependency Ardıcıllığı

Fixtures aşağıdakı ardıcıllıqla yüklənməlidir (management command avtomatik edir):

```
01_departments → 02_accounts → 03_competencies → 04_evaluations →
05_training → 06_development_plans → 07_workforce_planning →
08_continuous_feedback → 09_support
```

## Database-i Təmizləmək

Fixtures-i yenidən yükləməzdən əvvəl database-i təmizləmək üçün:

```bash
# SQLite üçün
python manage.py flush --no-input

# Və ya migrate 0
python manage.py migrate accounts zero
python manage.py migrate departments zero
# və s.

# Sonra yenidən migrate
python manage.py migrate
```

## Əlavə Məlumat

- Bütün password-lar demo üçün sadələşdirilmiş "password" olaraq təyin edilib
- MPTT (departments) və simple-history extensionları dəstəklənir
- Fixture-lərdə real Azərbaycan təşkilat strukturları simulyasiya edilib
- İstifadəçi dataları fictiv, real şəxslər deyil

## Problemlər

Əgər fixture yüklənərkən xəta alsanız:

1. **Duplicate key error**: Database-də artıq data var. `flush` edin
2. **Foreign key error**: Fixtures ardıcıllığı pozulub. Management command istifadə edin
3. **File not found**: Fixtures qovluğunun yolunu yoxlayın

Daha ətraflı məlumat üçün: `python manage.py load_initial_data --help`
