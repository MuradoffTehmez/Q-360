# 🚀 Q360 Production Deployment Checklist

## 📋 Sistemin Hazırlıq Vəziyyəti: **85%**

---

## ✅ HAZıR OLAN KOMPONENTLəR

### 1. **Əsas Funksionallıq** ✅
- ✅ İstifadəçi idarəetməsi və RBAC
- ✅ 360° qiymətləndirmə sistemi
- ✅ Hesabat və analitika
- ✅ Bildiriş sistemi
- ✅ Audit və təhlükəsizlik logları
- ✅ OKR/KPI idarəetməsi
- ✅ Təlim idarəetməsi
- ✅ İşə qəbul sistemi
- ✅ Kompensasiya idarəetməsi
- ✅ Məzuniyyət və iştirak

### 2. **Təhlükəsizlik** ✅ (Partial)
- ✅ Password validation
- ✅ CSRF protection
- ✅ XSS protection
- ✅ SQL Injection protection (Django ORM)
- ✅ JWT authentication
- ✅ Session security
- ✅ Audit logging
- ⚠️ SSL/HTTPS (production üçün konfiqurasiya lazımdır)
- ⚠️ Rate limiting (aktiv edilməlidir)
- ⚠️ 2FA (əlavə edilməlidir)

### 3. **Database** ✅
- ✅ Models təyin edilib
- ✅ Migrations hazırdır
- ✅ Relationships düzgündür
- ✅ Indexlər əlavə edilib
- ⚠️ SQLite → PostgreSQL miqrasiyası lazımdır

### 4. **Frontend** ✅
- ✅ Responsive dizayn
- ✅ Modern UI/UX
- ✅ Jazzmin admin panel
- ✅ i18n dəstəyi (AZ/EN)
- ✅ AJAX funksionallığı

### 5. **Logging** ✅
- ✅ Professional logging konfiqurasiyası
- ✅ Rotating file handlers
- ✅ Separate logs (error, security, api, celery)
- ✅ Console və file logging

---

## ⚠️ TƏKMİLLəŞDİRİLMƏLİ SAHƏLƏR

### 1. **Təhlükəsizlik Konfiqurasiyası** (KRİTİK)

#### 🔴 **Dərhal Düzəldilməli:**
```python
# .env faylında:
SECRET_KEY=<50+ simvoldan ibarət təsadüfi key>  # ❌ Hazırda zəif
DEBUG=False  # ❌ Hazırda True
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com  # ❌ Hazırda '*'
```

#### 🟡 **SSL/HTTPS Konfiqurasiyası:**
```bash
# settings.py-də (DEBUG=False olanda avtomatik aktiv olur):
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

#### 🟡 **Rate Limiting:**
```python
# settings.py-də aktivləşdirmək lazımdır:
# django-ratelimit yüklənməlidir
pip install django-ratelimit

# Middleware əlavə et:
MIDDLEWARE += ['django_ratelimit.middleware.RatelimitMiddleware']
```

### 2. **Database Migration** (KRİTİK)

#### SQLite → PostgreSQL
```bash
# 1. PostgreSQL quraşdırın
sudo apt-get install postgresql postgresql-contrib

# 2. Database yaradın
sudo -u postgres psql
CREATE DATABASE q360_db;
CREATE USER q360_user WITH PASSWORD 'strong_password_here';
ALTER ROLE q360_user SET client_encoding TO 'utf8';
ALTER ROLE q360_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE q360_user SET timezone TO 'Asia/Baku';
GRANT ALL PRIVILEGES ON DATABASE q360_db TO q360_user;
\q

# 3. .env faylını yeniləyin
DB_NAME=q360_db
DB_USER=q360_user
DB_PASSWORD=strong_password_here
DB_HOST=localhost
DB_PORT=5432

# 4. settings.py-də PostgreSQL konfiqurasiyasını aktivləşdirin
# (sətirlər 112-121 arası comment-ləri silin)

# 5. Data transfer
python manage.py dumpdata > data.json
# PostgreSQL-ə keçdikdən sonra:
python manage.py loaddata data.json
```

### 3. **Redis və Caching** (YÜKSəK PRİORİTET)

```bash
# 1. Redis quraşdırın
sudo apt-get install redis-server

# 2. django-redis yüklənib (requirements.txt-də var)
# 3. settings.py-də Redis cache konfiqurasiyasını aktivləşdirin
# (sətirlər 253-270 arası comment-ləri silin)

# 4. Celery üçün Redis
# .env faylında:
REDIS_URL=redis://localhost:6379/0
```

### 4. **Celery və Background Tasks**

```bash
# 1. Celery worker başlatın
celery -A config worker -l info

# 2. Celery beat başlatın (scheduled tasks)
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

# 3. Supervisor ilə avtomatik başlatma (production)
sudo apt-get install supervisor

# /etc/supervisor/conf.d/q360_celery.conf
[program:q360_celery]
command=/path/to/venv/bin/celery -A config worker -l info
directory=/path/to/q360_project
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/celery/worker.log

[program:q360_celery_beat]
command=/path/to/venv/bin/celery -A config beat -l info
directory=/path/to/q360_project
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/celery/beat.log
```

### 5. **Static və Media Fayllar**

```bash
# 1. Static faylları toplama
python manage.py collectstatic --noinput

# 2. Whitenoise aktivləşdirin (requirements.txt-də var)
# settings.py-də (sətr 65):
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# settings.py-də (sətr 169):
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 3. Media fayllar üçün ayrıca storage (AWS S3 və ya local)
# Böyük proyektlər üçün AWS S3 tövsiyə olunur:
pip install django-storages boto3
```

### 6. **Email Konfiqurasiyası**

```bash
# .env faylında:
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com  # və ya corporate SMTP
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@company.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@q360system.com
```

### 7. **Web Server Konfiqurasiyası**

#### **Nginx + Gunicorn**
```bash
# 1. Gunicorn yüklənib (requirements.txt-də var)

# 2. Gunicorn socket faylı yaradın
# /etc/systemd/system/q360.socket
[Unit]
Description=Q360 gunicorn socket

[Socket]
ListenStream=/run/q360.sock

[Install]
WantedBy=sockets.target

# 3. Gunicorn service faylı
# /etc/systemd/system/q360.service
[Unit]
Description=Q360 gunicorn daemon
Requires=q360.socket
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
RuntimeDirectory=gunicorn
WorkingDirectory=/var/www/q360_project
ExecStart=/var/www/q360_project/venv/bin/gunicorn \
          --access-logfile - \
          --workers 4 \
          --bind unix:/run/q360.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target

# 4. Nginx konfiqurasiyası
# /etc/nginx/sites-available/q360
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Static files
    location /static/ {
        alias /var/www/q360_project/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /var/www/q360_project/media/;
        expires 7d;
    }

    # Django application
    location / {
        proxy_pass http://unix:/run/q360.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Security: deny access to sensitive files
    location ~ /\. {
        deny all;
    }

    # Max upload size
    client_max_body_size 50M;
}

# 5. SSL sertifikat (Let's Encrypt)
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 8. **Backup Strategy**

```bash
# 1. Database backup skripti
# /opt/scripts/backup_q360.sh
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/q360"
DB_NAME="q360_db"

# PostgreSQL backup
pg_dump -U q360_user $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Media files backup
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/q360_project/media/

# Keep last 30 days
find $BACKUP_DIR -type f -mtime +30 -delete

# 2. Crontab əlavə edin
0 2 * * * /opt/scripts/backup_q360.sh
```

### 9. **Monitoring və Logging**

```bash
# 1. Sentry inteqrasiyası (error tracking)
pip install sentry-sdk

# settings.py:
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

if not DEBUG:
    sentry_sdk.init(
        dsn="your-sentry-dsn",
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )

# 2. Prometheus + Grafana (optional)
pip install django-prometheus

# 3. Log monitoring
# Logrotate konfiqurasiyası: /etc/logrotate.d/q360
/var/www/q360_project/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 www-data www-data
    sharedscripts
    postrotate
        systemctl reload nginx > /dev/null
    endscript
}
```

### 10. **Performance Optimization**

```python
# 1. Database optimization
# settings.py:
DATABASES['default']['CONN_MAX_AGE'] = 600  # Connection pooling

# 2. Query optimization
# select_related və prefetch_related istifadə edin

# 3. Cache views
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 dəqiqə
def my_view(request):
    ...

# 4. Database indexing
# Çox istifadə olunan field-lərə index əlavə edin:
class Meta:
    indexes = [
        models.Index(fields=['created_at', 'status']),
    ]
```

---

## 🚀 DEPLOYMENT ADDAMLARI

### **A. Server Hazırlığı**

```bash
# 1. Server yenilənməsi
sudo apt-get update && sudo apt-get upgrade -y

# 2. Lazımi paketlər
sudo apt-get install -y python3-pip python3-dev python3-venv \
    postgresql postgresql-contrib nginx redis-server \
    supervisor git build-essential libpq-dev

# 3. Firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

### **B. Proyekt Deploy**

```bash
# 1. Proyekt klonlama
cd /var/www
sudo git clone <your-repo-url> q360_project
sudo chown -R www-data:www-data q360_project

# 2. Virtual environment
cd q360_project
python3 -m venv venv
source venv/bin/activate

# 3. Dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Environment faylı
cp .env.example .env
nano .env  # Düzgün məlumatları daxil edin

# 5. Static fayllar
python manage.py collectstatic --noinput

# 6. Database
python manage.py migrate

# 7. Superuser yaratma
python manage.py createsuperuser

# 8. Permissions
sudo chown -R www-data:www-data /var/www/q360_project
sudo chmod -R 755 /var/www/q360_project
```

### **C. Services Başlatma**

```bash
# 1. Gunicorn
sudo systemctl start q360.socket
sudo systemctl enable q360.socket
sudo systemctl start q360.service
sudo systemctl enable q360.service

# 2. Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# 3. Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# 4. Celery
sudo systemctl start q360_celery
sudo systemctl enable q360_celery
sudo systemctl start q360_celery_beat
sudo systemctl enable q360_celery_beat

# 5. Status yoxlama
sudo systemctl status q360.service nginx redis-server
```

---

## 📝 POST-DEPLOYMENT YOXLAMA

### **1. Funksionallıq Testləri**
- [ ] İstifadəçi login/logout
- [ ] Qiymətləndirmə yaratma və cavablama
- [ ] Hesabat generasiyası
- [ ] Email göndərmə
- [ ] File upload/download
- [ ] Celery tasks işləyir
- [ ] Cache işləyir
- [ ] API endpoints

### **2. Təhlükəsizlik Testləri**
```bash
# SSL Test
curl -I https://yourdomain.com

# Security headers yoxlama
curl -I https://yourdomain.com | grep -E '(Strict-Transport|X-Frame|X-Content)'

# Django check
python manage.py check --deploy
```

### **3. Performance Testləri**
```bash
# Load testing (Apache Bench)
ab -n 1000 -c 100 https://yourdomain.com/

# Database query optimization
python manage.py debugsqlshell
```

---

## 📊 SİSTEM REQUİREMENTS

### **Minimum:**
- **CPU:** 2 core
- **RAM:** 4 GB
- **Disk:** 20 GB SSD
- **OS:** Ubuntu 20.04+ / Debian 11+

### **Tövsiyə Olunan:**
- **CPU:** 4+ core
- **RAM:** 8+ GB
- **Disk:** 50+ GB SSD
- **OS:** Ubuntu 22.04 LTS

---

## 🔗 FayDALı LİNKLƏR

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Best Practices](https://www.nginx.com/blog/nginx-best-practices/)
- [PostgreSQL Performance](https://www.postgresql.org/docs/current/performance-tips.html)

---

## ✅ FİNAL CHECKLIST

- [ ] DEBUG=False
- [ ] SECRET_KEY dəyişdirildi
- [ ] ALLOWED_HOSTS konfiqurasiya edildi
- [ ] PostgreSQL işləyir
- [ ] Redis işləyir
- [ ] Celery işləyir
- [ ] Nginx + Gunicorn işləyir
- [ ] SSL sertifikat quraşdırıldı
- [ ] Static fayllar collect edildi
- [ ] Email göndərmə test edildi
- [ ] Backup sistemi quruldu
- [ ] Monitoring/Logging aktiv
- [ ] Security headers əlavə edildi
- [ ] Firewall konfiqurasiyası
- [ ] Domain DNS təyin edildi

---

## 📞 DƏSTƏK

Deployment zamanı problem yaranarsa:
1. Logları yoxlayın: `/var/www/q360_project/logs/`
2. Nginx logları: `/var/log/nginx/`
3. Systemd logları: `sudo journalctl -u q360.service`
4. Celery logları: `/var/log/celery/`

---

**Son yeniləmə:** 2025-10-17
**Status:** 85% Hazır - Production deployment üçün yuxarıdakı addımları tamamlayın
