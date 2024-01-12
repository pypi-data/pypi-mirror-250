from django.db import models

from kfsd.apps.models.tables.relations.hrel import HRel
from kfsd.apps.models.tables.validations.policy import Policy


class Team(HRel):
    attrs = models.JSONField(default=dict)
    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.type = "Team"
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Team"
        verbose_name_plural = "Teams"
