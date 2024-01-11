from django.db import models

from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.settings.config import Config


def gen_local_id(configId):
    return configId


class Local(BaseModel):
    config = models.OneToOneField(
        Config, on_delete=models.CASCADE, related_name="local"
    )
    data = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        self.identifier = gen_local_id(self.config.identifier)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Local"
        verbose_name_plural = "Local"
