from django.db import models

from kfsd.apps.models.tables.relations.hrel import HRel
from kfsd.apps.models.tables.validations.policy import Policy
from kfsd.apps.models.constants import MAX_LENGTH


class Service(HRel):
    attrs = models.JSONField(default=dict)
    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    current_plan_id = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.type = "Service"
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Service"
        verbose_name_plural = "Services"
