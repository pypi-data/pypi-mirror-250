from django.db import models

from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.settings.config import Config


def gen_setting_id(name):
    return "{}={}".format("SETTING", name)


class Setting(BaseModel):
    name = models.CharField(max_length=MAX_LENGTH)
    config = models.ForeignKey(Config, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        self.identifier = gen_setting_id(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Setting"
        verbose_name_plural = "Settings"
