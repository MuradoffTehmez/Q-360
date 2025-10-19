from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("departments", "0012_remove_department_departments_department_tref4ab"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OnboardingTemplate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, verbose_name="Şablon Adı")),
                ("slug", models.SlugField(max_length=160, unique=True, verbose_name="Slug")),
                ("description", models.TextField(blank=True, verbose_name="Təsvir")),
                ("is_default", models.BooleanField(default=False, help_text="Yeni işçilər üçün avtomatik seçilən şablon.", verbose_name="Defolt Şablon")),
                ("is_active", models.BooleanField(default=True, verbose_name="Aktivdir")),
                ("review_cycle_offset_days", models.PositiveIntegerField(default=90, help_text="İşçinin start tarixindən neçə gün sonra qiymətləndirmə kampaniyası başlasın.", verbose_name="Performans Qiymətləndirmə Startı (gün)")),
                ("salary_review_offset_days", models.PositiveIntegerField(default=60, help_text="İşçinin start tarixindən neçə gün sonra maaş təklifi hazırlansın.", verbose_name="Maaş İcmalı Startı (gün)")),
                ("training_plan_offset_days", models.PositiveIntegerField(default=14, help_text="İşçinin start tarixindən neçə gün sonra təlim planı yaradılsın.", verbose_name="Təlim Planı Startı (gün)")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")),
            ],
            options={
                "ordering": ["name"],
                "verbose_name": "Onboarding Şablonu",
                "verbose_name_plural": "Onboarding Şablonları",
            },
        ),
        migrations.CreateModel(
            name="OnboardingTaskTemplate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Başlıq")),
                ("description", models.TextField(blank=True, verbose_name="Təsvir")),
                ("task_type", models.CharField(choices=[("general", "Ümumi Tapşırıq"), ("performance_review", "Performans Qiymətləndirmə Başlat"), ("salary_recommendation", "Maaş Artımı Tövsiyəsi"), ("training_plan", "Təlim Planı Yarat")], default="general", max_length=40, verbose_name="Tapşırıq Tipi")),
                ("due_in_days", models.PositiveIntegerField(default=7, help_text="Onboarding start tarixindən neçə gün sonra tamamlanmalıdır.", verbose_name="Son Tarix (gün)")),
                ("assignee_role", models.CharField(blank=True, choices=[("superadmin", "Super Administrator"), ("admin", "Administrator"), ("manager", "Menecer"), ("employee", "İşçi")], help_text="Boş olduqda tapşırıq işçiyə təyin ediləcək.", max_length=30, verbose_name="Məsul Rol")),
                ("auto_complete", models.BooleanField(default=False, help_text="İnteqrasiya uğurla başa çatdıqda tapşırıq avtomatik tamamlanır.", verbose_name="Avtomatik Tamamla")),
                ("metadata_schema", models.JSONField(blank=True, default=dict, help_text="İnteqrasiya məlumatları üçün JSON təsviri.", verbose_name="Metadata Sxemi")),
                ("order", models.PositiveIntegerField(default=1, verbose_name="Sıra")),
                ("template", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="task_templates", to="onboarding.onboardingtemplate", verbose_name="Şablon")),
            ],
            options={
                "ordering": ["order", "id"],
                "verbose_name": "Onboarding Tapşırıq Şablonu",
                "verbose_name_plural": "Onboarding Tapşırıq Şablonları",
            },
        ),
        migrations.CreateModel(
            name="OnboardingProcess",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start_date", models.DateField(default=django.utils.timezone.now, verbose_name="Başlama Tarixi")),
                ("status", models.CharField(choices=[("draft", "Qaralama"), ("active", "Aktiv"), ("completed", "Tamamlandı"), ("cancelled", "Ləğv edildi")], default="active", max_length=20, verbose_name="Status")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="initiated_onboarding_processes", to=settings.AUTH_USER_MODEL, verbose_name="Yaradan")),
                ("department", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="onboarding_processes", to="departments.department", verbose_name="Şöbə")),
                ("employee", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="onboarding_processes", to=settings.AUTH_USER_MODEL, verbose_name="İşçi")),
                ("template", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="processes", to="onboarding.onboardingtemplate", verbose_name="Şablon")),
            ],
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Onboarding Prosesi",
                "verbose_name_plural": "Onboarding Prosesləri",
                "unique_together": {("employee", "status")},
            },
        ),
        migrations.CreateModel(
            name="OnboardingTask",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Başlıq")),
                ("description", models.TextField(blank=True, verbose_name="Təsvir")),
                ("task_type", models.CharField(default="general", max_length=40, verbose_name="Tapşırıq Tipi")),
                ("due_date", models.DateField(blank=True, null=True, verbose_name="Son Tarix")),
                ("status", models.CharField(choices=[("pending", "Gözləyir"), ("in_progress", "İcrada"), ("completed", "Tamamlandı"), ("blocked", "Bloklanıb"), ("skipped", "Atlandı")], default="pending", max_length=20, verbose_name="Status")),
                ("metadata", models.JSONField(blank=True, default=dict, verbose_name="Əlavə Məlumat")),
                ("completed_at", models.DateTimeField(blank=True, null=True, verbose_name="Tamamlama Tarixi")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")),
                ("assigned_to", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="people_onboarding_tasks", to=settings.AUTH_USER_MODEL, verbose_name="Məsul Şəxs")),
                ("completed_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="completed_onboarding_tasks", to=settings.AUTH_USER_MODEL, verbose_name="Tamamlayan")),
                ("process", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tasks", to="onboarding.onboardingprocess", verbose_name="Prosess")),
                ("template_task", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="generated_tasks", to="onboarding.onboardingtasktemplate", verbose_name="Tapşırıq Şablonu")),
            ],
            options={
                "ordering": ["due_date", "id"],
                "verbose_name": "Onboarding Tapşırığı",
                "verbose_name_plural": "Onboarding Tapşırıqları",
            },
        ),
        migrations.CreateModel(
            name="MarketSalaryBenchmark",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Vəzifə / Rol")),
                ("role_level", models.CharField(choices=[("entry", "Başlanğıc"), ("mid", "Orta Səviyyə"), ("senior", "Təcrübəli"), ("lead", "Rəhbər")], default="mid", max_length=20, verbose_name="Səviyyə")),
                ("currency", models.CharField(default="AZN", max_length=3, verbose_name="Valyuta")),
                ("min_salary", models.DecimalField(decimal_places=2, max_digits=12, verbose_name="Minimum Maaş")),
                ("median_salary", models.DecimalField(decimal_places=2, max_digits=12, verbose_name="Median Maaş")),
                ("max_salary", models.DecimalField(decimal_places=2, max_digits=12, verbose_name="Maksimum Maaş")),
                ("data_source", models.CharField(blank=True, max_length=255, verbose_name="Məlumat Mənbəyi")),
                ("effective_date", models.DateField(default=django.utils.timezone.now, verbose_name="Tarix")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")),
                ("department", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="salary_benchmarks", to="departments.department", verbose_name="Şöbə")),
            ],
            options={
                "ordering": ["-effective_date", "title"],
                "verbose_name": "Market Maaş Benchmark",
                "verbose_name_plural": "Market Maaş Benchmarkları",
            },
        ),
        migrations.AddIndex(
            model_name="onboardingprocess",
            index=models.Index(fields=["status"], name="onboarding_status_08f1f6_idx"),
        ),
        migrations.AddIndex(
            model_name="onboardingprocess",
            index=models.Index(fields=["employee", "status"], name="onboarding_employee__5a9042_idx"),
        ),
        migrations.AddIndex(
            model_name="onboardingtask",
            index=models.Index(fields=["status"], name="onboarding_status_af082f_idx"),
        ),
        migrations.AddIndex(
            model_name="onboardingtask",
            index=models.Index(fields=["task_type"], name="onboarding_task_typ_d111cc_idx"),
        ),
        migrations.AddIndex(
            model_name="onboardingtask",
            index=models.Index(fields=["due_date"], name="onboarding_due_date_2ffdf8_idx"),
        ),
        migrations.AddIndex(
            model_name="marketsalarybenchmark",
            index=models.Index(fields=["title", "role_level"], name="onboarding_title_r_1e763a_idx"),
        ),
        migrations.AddIndex(
            model_name="marketsalarybenchmark",
            index=models.Index(fields=["department", "role_level"], name="onboarding_departme_640cb4_idx"),
        ),
        migrations.AddIndex(
            model_name="marketsalarybenchmark",
            index=models.Index(fields=["effective_date"], name="onboarding_effecti_5f7ea8_idx"),
        ),
    ]
