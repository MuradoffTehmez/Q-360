Context (Layihənin məqsədi):
Bu layihə dövlət sektorunda fəaliyyət göstərən qurumlar (nazirliklər, idarələr, şöbələr və s.) üçün nəzərdə tutulmuş 360 dərəcə qiymətləndirmə sistemidir. Sistem, dövlət qulluqçularının və əməkdaşların fəaliyyətini hərtərəfli, obyektiv və çox-mənbəli rəy mexanizmi vasitəsilə qiymətləndirəcək.
Məqsəd – işçilərin performansını rəhbər, həmkar, tabeliyində olan əməkdaş və özünüdəyərləndirmə əsasında təhlil edən, nəticələri avtomatik hesabatlara çevirən tam funksional bir HR qiymətləndirmə platforması yaratmaqdır.

🏗️ 1. Texnoloji Stack

Backend: Python 3.12+, Django 5.x, Django REST Framework
Frontend: Django Template (Bootstrap 5) və ya React (API ilə inteqrasiya)
Database: PostgreSQL
Asinxron Tapşırıqlar: Celery + Redis
Autentifikasiya: Django Auth + JWT (SimpleJWT paketi)
Deployment: Docker + Gunicorn + Nginx
Logging və Audit: Django Simple History, Logging Middleware
Security: HTTPS, CSRF, Role-based Access Control (RBAC), Environment Secrets

⚙️ 2. Əsas Modullar və App-lər

Layihə çoxmodullu Django arxitekturasında qurulmalıdır.
Hər modul (app) müstəqil “micro-layer” kimi işləməlidir:

Modul Məqsəd Əsas Modellər
accounts İstifadəçilərin qeydiyyatı, autentifikasiya, rollar User, Role, Permission, Profile
departments Dövlət strukturunun iyerarxik idarəsi Organization, Department, Position
evaluations Qiymətləndirmə kampaniyalarının və sualların idarəsi EvaluationCampaign, Question, Assignment, Response
notifications E-poçt və daxili bildirişlər Notification, EmailTemplate
reports Statistik və fərdi hesabatların yaradılması Report, RadarChartData, ScoreTrend
development_plans Fərdi İnkişaf Planlarının (IDP) idarəsi DevelopmentGoal, ProgressLog
audit Sistem hərəkətlərinin qeydiyyatı AuditLog, ActionTrail
🧩 3. Model Quruluşu (ORM Sxemi)

User modeli:

class User(AbstractUser):
    role = models.CharField(choices=[('admin','Admin'),('manager','Menecer'),('employee','İşçi')])
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE)
    position = models.CharField(max_length=100)

EvaluationCampaign modeli:

class EvaluationCampaign(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

Assignment modeli (kim kimi qiymətləndirir):

class EvaluationAssignment(models.Model):
    evaluator = models.ForeignKey(User, related_name='given_evaluations', on_delete=models.CASCADE)
    evaluatee = models.ForeignKey(User, related_name='received_evaluations', on_delete=models.CASCADE)
    campaign = models.ForeignKey(EvaluationCampaign, on_delete=models.CASCADE)

Question və Response modelləri:

class Question(models.Model):
    text = models.TextField()
    category = models.CharField(max_length=100)
    max_score = models.PositiveIntegerField(default=5)

class Response(models.Model):
    assignment = models.ForeignKey(EvaluationAssignment, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField(blank=True)

📊 4. Qiymətləndirmə Mexanizmi

Sistem “kampaniya” prinsipi ilə işləyəcək.

Superadmin yeni qiymətləndirmə dövrü (məsələn, “2025 Dövlət İllik Qiymətləndirmə”) yaradır.

Hər kampaniya üçün kim kimi dəyərləndirəcəyini təyin edir.

Sistem avtomatik olaraq qiymətləndirmə formalarını generasiya edir.

İstifadəçilər öz hesablarına daxil olub özünüqiymətləndirmə və başqalarını qiymətləndirmə formalarını doldururlar.

Suallar 1-5 arası bal və ya “Bəli/Xeyr” formasında cavablandırılır.

Cavablar saxlanıldıqdan sonra sistem avtomatik olaraq ortalama nəticələri və bal fərqlərini (self vs others) hesablayır.

🧠 5. Analitika və Hesabatlar

Hesabat növləri:

Fərdi Hesabat:

Radar Chart (kompetensiyalar üzrə ortalama bal)

Özünü və digərlərini müqayisə edən bal fərqləri

Anonim həmkar rəyləri

Ümumi Statistik Hesabat:

Bütün şöbələr üzrə orta göstəricilər

Departamentlərarası müqayisə

Qrafik trendlər (bar, line chart)

İxrac:

PDF və Excel fayllarına ixrac

Django reportlab və pandas kitabxanaları ilə

🔒 6. Təhlükəsizlik və Məxfilik

Bütün şifrələr hash (PBKDF2 və ya Argon2) ilə saxlanılacaq.

Django settings-də SECRET_KEY, DB parolları .env faylında saxlanılacaq.

HTTPS + SSL aktiv olacaq.

JWT tokenlər ilə API autentifikasiyası (qısa ömürlü access, uzun ömürlü refresh token).

Anonimlik prinsipi: işçilərin verdiyi rəyin kimə aid olduğu yalnız superadmin tərəfindən baxıla biləcək.

django-simple-history ilə bütün dəyişikliklərin auditi aparılacaq.

📨 7. Bildiriş Sistemi

Celery vasitəsilə asinxron email göndəriş

E-poçt şablonları (django-templated-email)

Bildiriş növləri:

Yeni qiymətləndirmə tapşırığı

Kampaniya başlanğıcı / bitmə tarixi

Hesabat hazır olduqda xəbərdarlıq

🎨 8. UI/UX və Dizayn Prinsipləri

Dizayn müasir, sadə və adaptiv olacaq.

Bootstrap 5, Chart.js və DataTables istifadə ediləcək.

Rol əsaslı interfeys:

Superadmin: Ümumi idarəetmə, kampaniyalar, statistika

Admin: Öz təşkilat bölməsi üzrə istifadəçilər və nəticələr

Menecer: Komandasının qiymətləndirmələri və inkişaf planları

İşçi: Öz rəy formaları və fərdi hesabatı

🧱 9. API Nümunələri (Django REST Framework)

# evaluations/views.py

class EvaluationAssignmentViewSet(ModelViewSet):
    queryset = EvaluationAssignment.objects.all()
    serializer_class = EvaluationAssignmentSerializer
    permission_classes = [IsAuthenticated]

class SubmitResponseAPIView(APIView):
    def post(self, request):
        serializer = ResponseSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Responses saved successfully."}, status=201)
        return Response(serializer.errors, status=400)

☁️ 10. Deployment və Konfiqurasiya

Docker-compose tərkibi:

web: Django + Gunicorn

db: PostgreSQL

redis: Redis broker

celery: asinxron task worker

nginx: reverse proxy

docker-compose.yml faylında bütün servis mühitləri .env faylından oxunacaq.

GitHub Actions CI/CD pipeline əlavə ediləcək (test → build → deploy mərhələləri).

🔍 11. Gələcək Genişlənmə Planı

AI ilə avtomatik rəy analizi (NLP sentiment analysis)

Power BI və ya Grafana inteqrasiyası üçün REST API-lar

Mobil uyğun React Native interfeysi

Dövlət ID (ASAN Login və ya e-Gov SSO) ilə giriş inteqrasiyası

💡 AI üçün İstifadə Təsviri

Təlimat:
Sən professional bir Django developer kimi davran.
Dövlət sektoru üçün nəzərdə tutulmuş 360 Dərəcə Qiymətləndirmə Sistemi yarat.
Aşağıdakı tələblərə uyğun tam backend strukturu, model kodları, API-lar, UI səhifələri və Docker mühitini avtomatik generasiya et.
Sistem müasir, təhlükəsiz və genişlənə bilən olmalıdır.
Kod PEP8 standartlarına, OOP prinsiplərinə, və REST dizayn qaydalarına tam cavab verməlidir.

Əlavə olaraq:

Admin panelini django-jazzmin ilə təkmilləşdir.

Hesabat generasiyasını reportlab ilə PDF formatında et.

Fərdi inkişaf planı (IDP) bölməsini ayrıca app kimi əlavə et.

Bütün verilənlər bazası modelləri üçün __str__ və Meta sinifləri daxil et.
