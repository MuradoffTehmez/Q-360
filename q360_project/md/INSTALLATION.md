# Q360 Quraşdırma Təlimatı

## Sistem Tələbləri

- **Python**: 3.12 və ya daha yüksək
- **PostgreSQL**: 14+
- **Redis**: 6+
- **Docker**: 20+ (Docker Compose ilə)
- **RAM**: Minimum 4GB
- **Disk**: Minimum 10GB boş yer

## Quraşdırma Metodları

### Method 1: Docker ilə (Tövsiyə edilir)

#### 1. Repository-ni klonlayın
```bash
git clone <repository-url>
cd q360_project
```

#### 2. Environment faylını konfiqurasiya edin
```bash
cp .env.example .env
nano .env  # və ya istənilən redaktor
```

Aşağıdakı parametrləri mütləq dəyişdirin:
```env
SECRET_KEY=your-unique-secret-key-min-50-characters
DB_PASSWORD=strong_database_password
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-app-password
```

#### 3. Docker konteynerləri qaldırın
```bash
docker-compose up -d --build
```

Bu komanda aşağıdakı servləri qaldıracaq:
- PostgreSQL database
- Redis cache/broker
- Django web application
- Celery worker
- Celery beat scheduler
- Nginx reverse proxy

#### 4. Database migrationslarını icra edin
```bash
docker-compose exec web python manage.py migrate
```

#### 5. Superuser yaradın
```bash
docker-compose exec web python manage.py createsuperuser
```

Sorğulara cavab verin:
- Username
- Email
- Password

#### 6. Statik faylları toplayın
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

#### 7. İlk data yükləyin (opsional)
```bash
docker-compose exec web python manage.py loaddata initial_data
```

#### 8. Sistemə daxil olun
```
Admin Panel: http://localhost/admin
API: http://localhost/api
```

---

### Method 2: Manual Quraşdırma

#### 1. PostgreSQL quraşdırın
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Windows
# PostgreSQL rəsmi saytından yükləyin
```

#### 2. Database yaradın
```bash
sudo -u postgres psql
CREATE DATABASE q360_db;
CREATE USER q360user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE q360_db TO q360user;
\q
```

#### 3. Redis quraşdırın
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Start redis
redis-server
```

#### 4. Python virtual environment yaradın
```bash
python3.12 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

#### 5. Python paketlərini quraşdırın
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 6. .env faylını yaradın
```bash
cp .env.example .env
# Faylı redaktə edin və parametrləri dəyişdirin
```

#### 7. Migrations icra edin
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 8. Superuser yaradın
```bash
python manage.py createsuperuser
```

#### 9. Statik faylları toplayın
```bash
python manage.py collectstatic
```

#### 10. Development serveri başladın
```bash
python manage.py runserver
```

#### 11. Celery-ni başladın (ayrı terminalda)
```bash
# Worker
celery -A config worker -l info

# Beat scheduler (ayrı terminalda)
celery -A config beat -l info
```

---

## İlk Konfiqurasiya

### 1. Admin Panel-ə Daxil Olun
```
URL: http://localhost:8000/admin
Username: (yaratdığınız superuser)
Password: (yaratdığınız şifrə)
```

### 2. Təşkilat Yaradın
1. Admin paneldə "Təşkilatlar" bölməsinə gedin
2. "Yeni Təşkilat" düyməsinə basın
3. Formanı doldurun:
   - Təşkilat Adı
   - Qısa Ad
   - Təşkilat Kodu
   - Əlaqə məlumatları

### 3. Şöbələri Əlavə Edin
1. "Şöbələr" bölməsinə gedin
2. Hər şöbə üçün:
   - Şöbə adı
   - Kod
   - Üst şöbə (varsa)
   - Şöbə rəhbəri

### 4. Vəzifələri Müəyyən Edin
1. "Vəzifələr" bölməsində vəzifələri yaradın
2. Hər vəzifə üçün səviyyə təyin edin

### 5. İstifadəçiləri Yaradın
1. "İstifadəçilər" bölməsinə gedin
2. Toplu import və ya fərdi əlavə edin
3. Hər istifadəçi üçün:
   - Şəxsi məlumatlar
   - Rol (Admin, Menecer, İşçi)
   - Şöbə
   - Vəzifə
   - Rəhbər

### 6. Sual Kateqoriyaları
1. "Sual Kateqoriyaları" yaradın:
   - Rəhbərlik
   - Kommunikasiya
   - Texniki Bacarıqlar
   - Komanda İşi
   - və s.

### 7. Sualları Əlavə Edin
1. Hər kateqoriya üçün suallar yaradın
2. Sual növünü seçin (Bal, Bəli/Xeyr, Açıq cavab)
3. Maksimum bal təyin edin

### 8. Qiymətləndirmə Kampaniyası
1. "Qiymətləndirmə Kampaniyaları" yaradın
2. Başlama və bitmə tarixlərini təyin edin
3. Sualları kampaniyaya əlavə edin
4. Hədəf şöbə və istifadəçiləri seçin
5. Qiymətləndirmə tapşırıqları yaradın
6. Kampaniyanı aktivləşdirin

---

## Production Deployment

### 1. Security Checklist
- [ ] SECRET_KEY-i dəyişdirin (min 50 simvol)
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS-u konfiqurasiya edin
- [ ] Database şifrəsini güclü edin
- [ ] HTTPS aktivləşdirin
- [ ] Firewall konfiqurasiyası
- [ ] Regular backup strategiyası

### 2. Environment Variables
```env
DEBUG=False
SECRET_KEY=<50-character-random-string>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_PASSWORD=<strong-password>
```

### 3. HTTPS Konfiqurasiyası
```bash
# SSL sertifikatı əldə edin (Let's Encrypt)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 4. Nginx Konfiqurasiyası (Production)
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # ... digər konfiqurasiya
}
```

### 5. Monitoring və Logging
```bash
# Log fayllarını yoxlayın
docker-compose logs -f web
docker-compose logs -f celery

# Container statusunu yoxlayın
docker-compose ps
```

---

## Troubleshooting

### Database Connection Xətası
```bash
# Database servisin işlədiyini yoxlayın
docker-compose ps db

# Database logs
docker-compose logs db

# Yenidən başladın
docker-compose restart db
```

### Migration Xətaları
```bash
# Migrations vəziyyətini yoxlayın
python manage.py showmigrations

# Fake migration (lazım olduqda)
python manage.py migrate --fake-initial
```

### Static Files Problemi
```bash
# Yenidən collectstatic
docker-compose exec web python manage.py collectstatic --clear --noinput
```

### Celery İşləmir
```bash
# Redis işlədiyini yoxlayın
docker-compose exec redis redis-cli ping

# Celery worker yenidən başladın
docker-compose restart celery
```

---

## Backup və Restore

### Database Backup
```bash
# Backup
docker-compose exec db pg_dump -U q360user q360_db > backup_$(date +%Y%m%d).sql

# Restore
docker-compose exec -T db psql -U q360user q360_db < backup_20250101.sql
```

### Media Files Backup
```bash
# Backup
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/

# Restore
tar -xzf media_backup_20250101.tar.gz
```

---

## Performans Optimizasiyası

1. **Database Indexing**: Migration fayllarında index-lər əlavə edin
2. **Caching**: Redis cache aktivləşdirin
3. **Query Optimization**: select_related və prefetch_related istifadə edin
4. **Static Files**: CDN istifadə edin
5. **Database Connection Pooling**: PgBouncer quraşdırın

---

## Əlavə Resurslar

- Django Documentation: https://docs.djangoproject.com/
- DRF Documentation: https://www.django-rest-framework.org/
- Celery Documentation: https://docs.celeryproject.org/
- PostgreSQL Documentation: https://www.postgresql.org/docs/

---

## Dəstək

Problemlə qarşılaşdıqda:
1. Log fayllarını yoxlayın
2. Error mesajını oxuyun
3. Documentation-a baxın
4. GitHub issues-da axtarın
5. Texniki dəstəklə əlaqə saxlayın
