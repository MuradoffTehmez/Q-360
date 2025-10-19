from django.apps import AppConfig


class OnboardingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.onboarding"
    verbose_name = "Onboarding və Adaptasiya"

    def ready(self) -> None:
        # Import signal handlers so onboarding workflows hook into user creation.
        from . import signals  # noqa: F401

