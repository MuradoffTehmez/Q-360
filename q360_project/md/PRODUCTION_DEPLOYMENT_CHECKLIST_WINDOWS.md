# 🚀 Q360 Production Deployment Checklist - WINDOWS

## 📋 Sistemin Hazırlıq Vəziyyəti: **85%**

---

## ✅ HAZIR OLAN KOMPONENTLəR

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
- ⚠️ SQLite → PostgreSQL/MSSQL miqrasiyası lazımdır

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
```powershell
# .env faylında:
SECRET_KEY=<50+ simvoldan ibarət təsadüfi key>  # ❌ Hazırda zəif
DEBUG=False  # ❌ Hazırda True
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com  # ❌ Hazırda '*'
```

**Güclü SECRET_KEY yaratmaq:**
```powershell
# PowerShell istifadə edərək:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 🟡 **SSL/HTTPS Konfiqurasiyası:**
```python
# settings.py-də (DEBUG=False olanda avtomatik aktiv olur):
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

#### 🟡 **Rate Limiting:**
```powershell
# PowerShell (Administrator olaraq):
pip install django-ratelimit

# settings.py-də aktivləşdirmək:
MIDDLEWARE += ['django_ratelimit.middleware.RatelimitMiddleware']
```

### 2. **Database Migration** (KRİTİK)

#### **Variant 1: PostgreSQL (Tövsiyə olunur)**

```powershell
# 1. PostgreSQL yükləyin (Windows)
# https://www.postgresql.org/download/windows/
# və ya Chocolatey ilə:
choco install postgresql

# 2. PostgreSQL başladın
net start postgresql-x64-14

# 3. Database yaradın (PowerShell)
$env:PGPASSWORD='postgres_admin_password'
psql -U postgres -c "CREATE DATABASE q360_db;"
psql -U postgres -c "CREATE USER q360_user WITH PASSWORD 'strong_password_here';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE q360_db TO q360_user;"

# 4. .env faylını yeniləyin
DB_ENGINE=postgresql
DB_NAME=q360_db
DB_USER=q360_user
DB_PASSWORD=strong_password_here
DB_HOST=localhost
DB_PORT=5432

# 5. psycopg2 yükləyin
pip install psycopg2-binary

# 6. Data transfer
python manage.py dumpdata > data.json
# settings.py-də PostgreSQL konfiqurasiyasını aktivləşdirdikdən sonra:
python manage.py migrate
python manage.py loaddata data.json
```

#### **Variant 2: Microsoft SQL Server (Enterprise üçün)**

```powershell
# 1. SQL Server Express yükləyin
# https://www.microsoft.com/en-us/sql-server/sql-server-downloads

# 2. SQL Server Management Studio (SSMS) yükləyin
choco install sql-server-management-studio

# 3. Database yaradın (SSMS-də və ya PowerShell):
# SQL Server-ə qoşulun və aşağıdakı skripti işə salın:
# CREATE DATABASE q360_db;
# CREATE LOGIN q360_user WITH PASSWORD = 'strong_password_here';
# USE q360_db;
# CREATE USER q360_user FOR LOGIN q360_user;
# ALTER ROLE db_owner ADD MEMBER q360_user;

# 4. .env faylını yeniləyin
DB_ENGINE=mssql
DB_NAME=q360_db
DB_USER=q360_user
DB_PASSWORD=strong_password_here
DB_HOST=localhost
DB_PORT=1433

# 5. mssql-django yükləyin
pip install mssql-django

# 6. settings.py-də MSSQL konfiqurasiyası:
# DATABASES = {
#     'default': {
#         'ENGINE': 'mssql',
#         'NAME': os.getenv('DB_NAME'),
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': os.getenv('DB_HOST'),
#         'PORT': os.getenv('DB_PORT'),
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#         },
#     }
# }

# 7. ODBC Driver yükləyin
# https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
```

### 3. **Redis və Caching** (YÜKSəK PRİORİTET)

```powershell
# 1. Redis yükləyin (Windows)
# Memurai (Windows üçün Redis fork):
choco install memurai-developer

# Və ya Redis Windows versiyası:
# https://github.com/microsoftarchive/redis/releases

# 2. Redis başladın
net start Memurai

# 3. django-redis artıq yüklənib (requirements.txt-də var)

# 4. .env faylında
REDIS_URL=redis://localhost:6379/0

# 5. settings.py-də Redis cache konfiqurasiyasını aktivləşdirin
# (sətirlər 253-270 arası comment-ləri silin)
```

### 4. **Celery və Background Tasks (Windows)**

```powershell
# ⚠️ QEYD: Windows-da Celery 4.x+ problematikdir
# Tövsiyə olunan həllər:

# Variant 1: Windows Service Manager ilə (Tövsiyə)
# 1. NSSM (Non-Sucking Service Manager) yükləyin
choco install nssm

# 2. Celery worker servisi yaradın
nssm install Q360CeleryWorker "C:\lahiyeler\q360\venv\Scripts\celery.exe" "-A config worker -l info --pool=solo"
nssm set Q360CeleryWorker AppDirectory "C:\lahiyeler\q360\q360_project"
nssm set Q360CeleryWorker DisplayName "Q360 Celery Worker"
nssm set Q360CeleryWorker Description "Q360 Background Task Worker"
nssm set Q360CeleryWorker Start SERVICE_AUTO_START

# 3. Celery beat servisi yaradın
nssm install Q360CeleryBeat "C:\lahiyeler\q360\venv\Scripts\celery.exe" "-A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler"
nssm set Q360CeleryBeat AppDirectory "C:\lahiyeler\q360\q360_project"
nssm set Q360CeleryBeat DisplayName "Q360 Celery Beat"
nssm set Q360CeleryBeat Start SERVICE_AUTO_START

# 4. Servisleri başladın
nssm start Q360CeleryWorker
nssm start Q360CeleryBeat

# Variant 2: Eventlet ilə (Alternativ)
pip install eventlet
celery -A config worker -l info --pool=eventlet

# Variant 3: Gevent ilə
pip install gevent
celery -A config worker -l info --pool=gevent
```

### 5. **Static və Media Fayllar**

```powershell
# 1. Static faylları toplama
python manage.py collectstatic --noinput

# 2. Whitenoise aktivləşdirin (requirements.txt-də var)
# settings.py-də (sətr 65):
# MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# settings.py-də (sətr 169):
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 3. Media fayllar üçün ayrıca storage (Azure Blob və ya local)
# Azure Blob Storage (Windows üçün tövsiyə):
pip install django-storages[azure]

# settings.py:
# DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
# AZURE_ACCOUNT_NAME = 'your_account_name'
# AZURE_ACCOUNT_KEY = 'your_account_key'
# AZURE_CONTAINER = 'media'
```

### 6. **Email Konfiqurasiyası**

```powershell
# .env faylında:
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.office365.com  # və ya smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@company.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@q360system.com

# Office 365 üçün:
# EMAIL_HOST=smtp.office365.com
# EMAIL_PORT=587

# Gmail üçün (App Password lazımdır):
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
```

### 7. **Web Server Konfiqurasiyası - IIS (Internet Information Services)**

#### **IIS ilə Django Deploy**

```powershell
# 1. IIS və lazımi komponentləri quraşdırın
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServer
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CommonHttpFeatures
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpErrors
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpRedirect
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ApplicationDevelopment
Enable-WindowsOptionalFeature -Online -FeatureName IIS-NetFxExtensibility45
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HealthAndDiagnostics
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpLogging
Enable-WindowsOptionalFeature -Online -FeatureName IIS-LoggingLibraries
Enable-WindowsOptionalFeature -Online -FeatureName IIS-RequestMonitor
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpTracing
Enable-WindowsOptionalFeature -Online -FeatureName IIS-Security
Enable-WindowsOptionalFeature -Online -FeatureName IIS-RequestFiltering
Enable-WindowsOptionalFeature -Online -FeatureName IIS-Performance
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerManagementTools
Enable-WindowsOptionalFeature -Online -FeatureName IIS-IIS6ManagementCompatibility
Enable-WindowsOptionalFeature -Online -FeatureName IIS-Metabase
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ManagementConsole
Enable-WindowsOptionalFeature -Online -FeatureName IIS-BasicAuthentication
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WindowsAuthentication
Enable-WindowsOptionalFeature -Online -FeatureName IIS-StaticContent
Enable-WindowsOptionalFeature -Online -FeatureName IIS-DefaultDocument
Enable-WindowsOptionalFeature -Online -FeatureName IIS-DirectoryBrowsing
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebSockets
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ApplicationInit
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ISAPIExtensions
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ISAPIFilter
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpCompressionStatic

# 2. wfastcgi yükləyin
pip install wfastcgi
wfastcgi-enable

# 3. web.config faylı yaradın (C:\lahiyeler\q360\q360_project\web.config)
```

**web.config faylı:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <handlers>
            <add name="PythonHandler"
                 path="*"
                 verb="*"
                 modules="FastCgiModule"
                 scriptProcessor="C:\lahiyeler\q360\venv\Scripts\python.exe|C:\lahiyeler\q360\venv\Lib\site-packages\wfastcgi.py"
                 resourceType="Unspecified"
                 requireAccess="Script" />
        </handlers>
        <rewrite>
            <rules>
                <rule name="Static Files" stopProcessing="true">
                    <match url="^static/.*" />
                    <action type="Rewrite" url="{R:0}" logRewrittenUrl="false" />
                </rule>
                <rule name="Configure Python" stopProcessing="true">
                    <match url="(.*)" />
                    <conditions>
                        <add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" />
                    </conditions>
                    <action type="Rewrite" url="handler.fcgi/{R:1}" appendQueryString="true" />
                </rule>
            </rules>
        </rewrite>
        <staticContent>
            <mimeMap fileExtension=".json" mimeType="application/json" />
            <mimeMap fileExtension=".woff" mimeType="application/font-woff" />
            <mimeMap fileExtension=".woff2" mimeType="application/font-woff2" />
        </staticContent>
        <httpProtocol>
            <customHeaders>
                <add name="X-Frame-Options" value="DENY" />
                <add name="X-Content-Type-Options" value="nosniff" />
                <add name="X-XSS-Protection" value="1; mode=block" />
                <add name="Strict-Transport-Security" value="max-age=31536000; includeSubDomains; preload" />
            </customHeaders>
        </httpProtocol>
        <security>
            <requestFiltering>
                <requestLimits maxAllowedContentLength="52428800" /> <!-- 50MB -->
            </requestFiltering>
        </security>
    </system.webServer>
    <appSettings>
        <add key="WSGI_HANDLER" value="config.wsgi.application" />
        <add key="PYTHONPATH" value="C:\lahiyeler\q360\q360_project" />
        <add key="DJANGO_SETTINGS_MODULE" value="config.settings" />
    </appSettings>
</configuration>
```

**IIS-də Site yaratma:**
```powershell
# PowerShell (Administrator olaraq):
Import-Module WebAdministration

# Application Pool yaradın
New-WebAppPool -Name "Q360AppPool"
Set-ItemProperty IIS:\AppPools\Q360AppPool -Name "managedRuntimeVersion" -Value ""

# Web Site yaradın
New-Website -Name "Q360" -Port 80 -PhysicalPath "C:\lahiyeler\q360\q360_project" -ApplicationPool "Q360AppPool"

# Static files üçün virtual directory
New-WebVirtualDirectory -Site "Q360" -Name "static" -PhysicalPath "C:\lahiyeler\q360\q360_project\staticfiles"
New-WebVirtualDirectory -Site "Q360" -Name "media" -PhysicalPath "C:\lahiyeler\q360\q360_project\media"

# Permissions
icacls "C:\lahiyeler\q360\q360_project" /grant "IIS AppPool\Q360AppPool:(OI)(CI)F" /T
icacls "C:\lahiyeler\q360\q360_project\media" /grant "IIS AppPool\Q360AppPool:(OI)(CI)F" /T
icacls "C:\lahiyeler\q360\q360_project\logs" /grant "IIS AppPool\Q360AppPool:(OI)(CI)F" /T
```

#### **SSL Sertifikat (Let's Encrypt - Windows)**

```powershell
# 1. Win-ACME yükləyin
choco install win-acme

# 2. SSL sertifikat əldə edin
wacs.exe --target manual --host yourdomain.com --webroot "C:\lahiyeler\q360\q360_project"

# 3. IIS-də HTTPS binding əlavə edin
New-WebBinding -Name "Q360" -IP "*" -Port 443 -Protocol https
```

### 8. **Backup Strategy (Windows)**

```powershell
# backup_q360.ps1 skripti yaradın
# C:\Scripts\backup_q360.ps1

$DATE = Get-Date -Format "yyyyMMdd_HHmmss"
$BACKUP_DIR = "C:\Backups\Q360"
$DB_NAME = "q360_db"
$MEDIA_PATH = "C:\lahiyeler\q360\q360_project\media"

# Backup qovluğu yaradın
New-Item -ItemType Directory -Force -Path $BACKUP_DIR

# PostgreSQL backup
$env:PGPASSWORD = "your_password"
& "C:\Program Files\PostgreSQL\14\bin\pg_dump.exe" -U q360_user -h localhost $DB_NAME | Out-File "$BACKUP_DIR\db_$DATE.sql"

# Və ya SQL Server backup (SSMS-də və ya T-SQL):
# BACKUP DATABASE q360_db TO DISK = 'C:\Backups\Q360\db_$DATE.bak'

# Media faylları backup (ZIP)
Compress-Archive -Path $MEDIA_PATH -DestinationPath "$BACKUP_DIR\media_$DATE.zip"

# Köhnə backupları silin (30 gündən əvvəlki)
Get-ChildItem -Path $BACKUP_DIR -Recurse -File | Where-Object CreationTime -lt (Get-Date).AddDays(-30) | Remove-Item

# Log faylı
Add-Content -Path "$BACKUP_DIR\backup_log.txt" -Value "$(Get-Date) - Backup completed: db_$DATE.sql, media_$DATE.zip"
```

**Task Scheduler ilə avtomatik backup:**
```powershell
# PowerShell (Administrator olaraq):
$action = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument '-File C:\Scripts\backup_q360.ps1'
$trigger = New-ScheduledTaskTrigger -Daily -At 2am
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -Action $action -Trigger $trigger -Principal $principal -TaskName "Q360 Daily Backup" -Description "Daily backup for Q360 database and media files"
```

### 9. **Monitoring və Logging (Windows)**

```powershell
# 1. Sentry inteqrasiyası (error tracking)
pip install sentry-sdk

# settings.py:
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
#
# if not DEBUG:
#     sentry_sdk.init(
#         dsn="your-sentry-dsn",
#         integrations=[DjangoIntegration()],
#         traces_sample_rate=1.0,
#         send_default_pii=True
#     )

# 2. Windows Event Log inteqrasiyası
# settings.py-də LOGGING konfiqurasiyasına əlavə:
# 'handlers': {
#     'event_log': {
#         'level': 'ERROR',
#         'class': 'logging.handlers.NTEventLogHandler',
#         'appname': 'Q360System',
#     },
# }

# 3. Performance Monitor (PerfMon) ilə izləmək
# perfmon.exe açın və aşağıdakı counterləri əlavə edin:
# - Processor(_Total)\% Processor Time
# - Memory\Available MBytes
# - LogicalDisk(C:)\% Free Space
# - Web Service(_Total)\Current Connections
```

### 10. **Performance Optimization (Windows)**

```python
# settings.py optimizasiyaları:

# 1. Database connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 600

# 2. Windows üçün DEBUG=False zamanı
if not DEBUG:
    # Disable browsable API
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.JSONRenderer',
    ]

    # Use production-ready session engine
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

    # Template caching
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]

# 3. Gzip compression (IIS-də)
# web.config-ə əlavə edin:
# <httpCompression>
#     <dynamicTypes>
#         <add mimeType="text/*" enabled="true" />
#         <add mimeType="application/json" enabled="true" />
#     </dynamicTypes>
# </httpCompression>
```

---

## 🚀 DEPLOYMENT ADDAMLARI (WINDOWS)

### **A. Server Hazırlığı**

```powershell
# PowerShell (Administrator olaraq):

# 1. Chocolatey yükləyin (Windows package manager)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 2. Lazımi paketləri yükləyin
choco install python -y
choco install git -y
choco install postgresql -y  # və ya sql-server-express
choco install memurai-developer -y  # Redis alternative
choco install nssm -y  # Service manager

# 3. Firewall qaydaları
New-NetFirewallRule -DisplayName "Q360 HTTP" -Direction Inbound -LocalPort 80 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "Q360 HTTPS" -Direction Inbound -LocalPort 443 -Protocol TCP -Action Allow
```

### **B. Proyekt Deploy**

```powershell
# 1. Proyekt klonlama
cd C:\
New-Item -ItemType Directory -Force -Path "C:\inetpub\wwwroot\q360"
cd "C:\inetpub\wwwroot\q360"
git clone <your-repo-url> .

# Və ya proyekti kopyalayın:
Copy-Item -Path "C:\lahiyeler\q360\*" -Destination "C:\inetpub\wwwroot\q360\" -Recurse

# 2. Virtual environment
cd "C:\inetpub\wwwroot\q360"
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Environment faylı
Copy-Item .env.example .env
notepad .env  # Düzgün məlumatları daxil edin

# 5. Qovluqları yaradın
New-Item -ItemType Directory -Force -Path "logs"
New-Item -ItemType Directory -Force -Path "media"
New-Item -ItemType Directory -Force -Path "staticfiles"

# 6. Static fayllar
python manage.py collectstatic --noinput

# 7. Database
python manage.py migrate

# 8. Superuser yaratma
python manage.py createsuperuser

# 9. Permissions (IIS Application Pool istifadəçisi üçün)
icacls "C:\inetpub\wwwroot\q360" /grant "IIS AppPool\Q360AppPool:(OI)(CI)F" /T
icacls "C:\inetpub\wwwroot\q360\media" /grant "IIS AppPool\Q360AppPool:(OI)(CI)F" /T
icacls "C:\inetpub\wwwroot\q360\logs" /grant "IIS AppPool\Q360AppPool:(OI)(CI)F" /T
icacls "C:\inetpub\wwwroot\q360\db.sqlite3" /grant "IIS AppPool\Q360AppPool:(OI)(CI)F" /T
```

### **C. Services Başlatma**

```powershell
# 1. IIS
Start-Service W3SVC
Set-Service W3SVC -StartupType Automatic

# 2. PostgreSQL (və ya SQL Server)
Start-Service postgresql-x64-14
Set-Service postgresql-x64-14 -StartupType Automatic

# 3. Redis (Memurai)
Start-Service Memurai
Set-Service Memurai -StartupType Automatic

# 4. Celery (NSSM ilə yaradılıbsa)
nssm start Q360CeleryWorker
nssm start Q360CeleryBeat

# 5. Status yoxlama
Get-Service W3SVC, postgresql-x64-14, Memurai | Format-Table -AutoSize
```

---

## 📝 POST-DEPLOYMENT YOXLAMA

### **1. Funksionallıq Testləri**
```powershell
# PowerShell istifadə edərək:

# Web saytın açılmasını yoxlayın
Invoke-WebRequest -Uri "http://localhost" -UseBasicParsing

# HTTPS yoxlaması
Invoke-WebRequest -Uri "https://yourdomain.com" -UseBasicParsing

# API endpoint test
Invoke-RestMethod -Uri "http://localhost/api/health/" -Method GET
```

**Manual testlər:**
- [ ] İstifadəçi login/logout
- [ ] Qiymətləndirmə yaratma və cavablama
- [ ] Hesabat generasiyası
- [ ] Email göndərmə
- [ ] File upload/download
- [ ] Celery tasks işləyir
- [ ] Cache işləyir
- [ ] API endpoints

### **2. Təhlükəsizlik Testləri**
```powershell
# Django deployment check
python manage.py check --deploy

# IIS konfiqurasiyasını yoxlayın
Get-WebConfiguration -Filter '/system.webServer/httpProtocol/customHeaders'

# SSL sertifikat yoxlaması (PowerShell 7+)
$cert = Get-ChildItem -Path Cert:\LocalMachine\WebHosting | Where-Object { $_.Subject -like "*yourdomain.com*" }
$cert | Format-List Subject, NotAfter, Thumbprint
```

### **3. Performance Testləri**
```powershell
# Load testing (Visual Studio Load Test və ya JMeter istifadə edin)
# Və ya curl ilə:
for ($i=1; $i -le 100; $i++) {
    Measure-Command { Invoke-WebRequest -Uri "http://localhost" -UseBasicParsing }
}
```

---

## 📊 SİSTEM REQUİREMENTS (WINDOWS)

### **Minimum:**
- **OS:** Windows Server 2019+
- **CPU:** 2 core
- **RAM:** 4 GB
- **Disk:** 20 GB SSD
- **IIS:** 10.0+
- **.NET:** Framework 4.8+ (IIS üçün)

### **Tövsiyə Olunan:**
- **OS:** Windows Server 2022
- **CPU:** 4+ core
- **RAM:** 8+ GB
- **Disk:** 50+ GB SSD
- **IIS:** 10.0+
- **SQL Server:** 2019+

---

## 🔗 FAYДALI LİNKLƏR (WINDOWS)

- [Django on IIS](https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/iis/)
- [wfastcgi Documentation](https://pypi.org/project/wfastcgi/)
- [IIS Best Practices](https://docs.microsoft.com/en-us/iis/)
- [SQL Server Performance](https://docs.microsoft.com/en-us/sql/relational-databases/performance/)
- [Win-ACME (Let's Encrypt for Windows)](https://www.win-acme.com/)
- [NSSM Documentation](https://nssm.cc/)

---

## ✅ FINAL CHECKLIST (WINDOWS)

- [ ] DEBUG=False
- [ ] SECRET_KEY dəyişdirildi
- [ ] ALLOWED_HOSTS konfiqurasiya edildi
- [ ] PostgreSQL/MSSQL işləyir
- [ ] Redis (Memurai) işləyir
- [ ] Celery servislər işləyir
- [ ] IIS konfiqurasiya edilib
- [ ] SSL sertifikat quraşdırıldı
- [ ] Static fayllar collect edildi
- [ ] Email göndərmə test edildi
- [ ] Backup sistemi quruldu (Task Scheduler)
- [ ] Windows Event Log konfiqurasiyası
- [ ] Security headers əlavə edildi (web.config)
- [ ] Firewall qaydaları təyin edildi
- [ ] Domain DNS təyin edildi
- [ ] IIS Application Pool permissions verildi
- [ ] web.config düzgün konfiqurasiya edilib

---

## 🔧 TROUBLESHOOTING (WINDOWS)

### **Yaygin Problemlər və Həllər:**

#### 1. **"Access Denied" xətası**
```powershell
# IIS Application Pool-a tam icazə verin:
icacls "C:\inetpub\wwwroot\q360" /grant "IIS AppPool\Q360AppPool:(OI)(CI)F" /T
```

#### 2. **Celery Windows-da işləmir**
```powershell
# Eventlet və ya Gevent istifadə edin:
pip install eventlet
celery -A config worker -l info --pool=eventlet
```

#### 3. **Static fayllar yüklənmir**
```powershell
# IIS-də MIME types yoxlayın və virtual directory düzgün konfiqurasiya edin:
New-WebVirtualDirectory -Site "Q360" -Name "static" -PhysicalPath "C:\inetpub\wwwroot\q360\staticfiles"
```

#### 4. **Database bağlantı xətası**
```powershell
# PostgreSQL/SQL Server işlədiyinə əmin olun:
Get-Service | Where-Object {$_.Name -like "*sql*"}
Get-Service | Where-Object {$_.Name -like "*postgres*"}

# Bağlantını test edin:
Test-NetConnection -ComputerName localhost -Port 5432  # PostgreSQL
Test-NetConnection -ComputerName localhost -Port 1433  # SQL Server
```

#### 5. **Redis bağlantı xətası**
```powershell
# Memurai işlədiyinə əmin olun:
Get-Service Memurai

# Yenidən başladın:
Restart-Service Memurai
```

### **Log Faylları:**
- **IIS Logs:** `C:\inetpub\logs\LogFiles\`
- **Django Logs:** `C:\inetpub\wwwroot\q360\logs\`
- **Windows Event Log:** Event Viewer → Windows Logs → Application
- **Celery Logs:** NSSM konfiqurasiyasında təyin edilən path

---

## 📞 DƏSTƏK

Deployment zamanı problem yaranarsa:

1. **Django logları:** `C:\inetpub\wwwroot\q360\logs\`
2. **IIS logları:** `C:\inetpub\logs\LogFiles\`
3. **Event Viewer:** `eventvwr.msc` (Windows Logs → Application)
4. **Celery logları:** NSSM service logs

**Əlavə yardım:**
```powershell
# IIS konfiqurasiya test
Test-WebConfigFile -Path "C:\inetpub\wwwroot\q360\web.config"

# Service statusları
Get-Service | Where-Object {$_.DisplayName -like "*Q360*"}

# Port istifadəsi
Get-NetTCPConnection | Where-Object {$_.LocalPort -eq 80 -or $_.LocalPort -eq 443}
```

---

## ⚡ WINDOWS-SPESİFİK PERFORMANS TÖVSİYƏLƏRİ

### **1. IIS Application Pool Optimization:**
```powershell
# Application Pool Advanced Settings:
# - Queue Length: 1000 → 5000
# - Idle Time-out: 20 → 0 (Disable)
# - Regular Time Interval: 1740 → 0 (Disable recycling)
# - Start Mode: OnDemand → AlwaysRunning

Set-ItemProperty IIS:\AppPools\Q360AppPool -Name queueLength -Value 5000
Set-ItemProperty IIS:\AppPools\Q360AppPool -Name processModel.idleTimeout -Value "00:00:00"
Set-ItemProperty IIS:\AppPools\Q360AppPool -Name recycling.periodicRestart.time -Value "00:00:00"
Set-ItemProperty IIS:\AppPools\Q360AppPool -Name startMode -Value AlwaysRunning
```

### **2. Windows Disk I/O Optimization:**
```powershell
# Database və media fayllar üçün ayrı disk istifadə edin
# SSD istifadə edin
# Disk indexing-i söndürün (data disklərdə):
fsutil behavior set DisableLastAccess 1
```

### **3. Windows Defender Exclusions:**
```powershell
# Performans üçün proyekt qovluğunu exclude edin:
Add-MpPreference -ExclusionPath "C:\inetpub\wwwroot\q360"
Add-MpPreference -ExclusionPath "C:\Program Files\PostgreSQL"
Add-MpPreference -ExclusionPath "C:\Backups\Q360"
```

---

**Son yeniləmə:** 2025-10-17
**Status:** 85% Hazır - Production deployment üçün yuxarıdakı addımları tamamlayın
**Platform:** Windows Server 2019/2022
