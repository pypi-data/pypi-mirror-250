from django.db import models

from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.relations.hrel import HRel


def gen_access_id(actor, resource):
    return "ACTOR={},RESOURCE={}".format(actor.identifier, resource.identifier)


class Access(BaseModel):
    actor = models.ForeignKey(
        HRel, on_delete=models.CASCADE, related_name="actor_access"
    )
    resource = models.ForeignKey(
        HRel, on_delete=models.CASCADE, related_name="resource_access"
    )
    permissions = models.JSONField(default=list)

    def save(self, *args, **kwargs):
        self.identifier = gen_access_id(self.actor, self.resource)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Access"
        verbose_name_plural = "Accesses"
