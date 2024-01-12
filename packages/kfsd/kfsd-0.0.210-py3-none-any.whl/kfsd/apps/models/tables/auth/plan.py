from django.db import models

from kfsd.apps.models.tables.relations.hrel import HRel
from kfsd.apps.models.tables.validations.policy import Policy


class Plan(HRel):
    attrs = models.JSONField(default=dict)
    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.type = "Plan"
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
