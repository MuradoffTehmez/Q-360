from django.db import migrations


def create_default_template(apps, schema_editor):
    Template = apps.get_model("onboarding", "OnboardingTemplate")
    TaskTemplate = apps.get_model("onboarding", "OnboardingTaskTemplate")

    template, created = Template.objects.get_or_create(
        slug="standart-onboarding",
        defaults={
            "name": "Standart Onboarding Paketi",
            "description": "Yeni işçilər üçün avtomatik onboarding, performans və inkişaf axını.",
            "is_default": True,
            "is_active": True,
            "review_cycle_offset_days": 90,
            "salary_review_offset_days": 60,
            "training_plan_offset_days": 14,
        },
    )

    if not template.is_default:
        template.is_default = True
        template.save(update_fields=["is_default"])

    existing_titles = set(
        TaskTemplate.objects.filter(template=template).values_list("title", flat=True)
    )

    tasks = [
        {
            "title": "HR Onboarding Check-list",
            "description": "İşçinin profili, sənədləri və hesablanma məlumatlarını təsdiqləyin.",
            "task_type": "general",
            "due_in_days": 3,
            "assignee_role": "manager",
            "order": 1,
        },
        {
            "title": "İlkin performans qiymətləndirməsini planlaşdırın",
            "description": "Yeni işçinin onboarding dövrünün sonunda avtomatik 360° kampaniya yaradın.",
            "task_type": "performance_review",
            "due_in_days": template.review_cycle_offset_days,
            "assignee_role": "manager",
            "order": 2,
            "auto_complete": True,
            "metadata_schema": {
                "campaign_id": "int",
                "campaign_start": "date",
                "campaign_end": "date",
            },
        },
        {
            "title": "Market maaş təklifini hazırlayın",
            "description": "Market benchmark məlumatları əsasında maaş artımı tövsiyəsi hazırlayın.",
            "task_type": "salary_recommendation",
            "due_in_days": template.salary_review_offset_days,
            "assignee_role": "manager",
            "order": 3,
            "metadata_schema": {
                "benchmark_id": "int",
                "recommended_salary": "decimal",
                "increase_percentage": "decimal",
            },
        },
        {
            "title": "Skill gap təlim planı yaradın",
            "description": "Kompetensiya boşluqlarına uyğun təlim resurslarını təklif edin.",
            "task_type": "training_plan",
            "due_in_days": template.training_plan_offset_days,
            "assignee_role": "manager",
            "order": 4,
            "metadata_schema": {
                "competency_ids": "list[int]",
                "resource_recommendations": "list[object]",
            },
        },
    ]

    for task in tasks:
        if task["title"] in existing_titles:
            continue
        TaskTemplate.objects.create(template=template, **task)


def reverse_default_template(apps, schema_editor):
    Template = apps.get_model("onboarding", "OnboardingTemplate")
    TaskTemplate = apps.get_model("onboarding", "OnboardingTaskTemplate")

    try:
        template = Template.objects.get(slug="standart-onboarding")
    except Template.DoesNotExist:
        return

    TaskTemplate.objects.filter(template=template).delete()
    template.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("onboarding", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_template, reverse_default_template),
    ]

