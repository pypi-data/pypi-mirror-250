from django.apps import AppConfig


class ModelsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kfsd.apps.models"

    def ready(self):
        from . import signals  # noqa: F401
