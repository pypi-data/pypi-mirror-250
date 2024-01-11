from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.auth.base import BasePermHandler
from kfsd.apps.endpoints.serializers.auth.role import (
    RoleModelSerializer,
    RoleSharedViewSerializer,
)
from kfsd.apps.models.tables.auth.role import Role
from kfsd.apps.endpoints.handlers.relations.base import handle_pre_del_process


def gen_role_handler(instance):
    handler = RoleHandler(instance.identifier, False)
    qsData = RoleModelSerializer(instance=instance)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Role)
def process_post_save(sender, instance, created, **kwargs):
    handler = gen_role_handler(instance)
    if not instance.policy:
        handler.setPolicy()


@receiver(pre_delete, sender=Role)
def process_pre_del(sender, instance, **kwargs):
    handle_pre_del_process(instance)


class RoleHandler(BasePermHandler):
    def __init__(self, roleIdentifier, isDBFetch):
        BasePermHandler.__init__(
            self,
            serializer=RoleModelSerializer,
            viewSerializer=RoleSharedViewSerializer,
            modelClass=Role,
            identifier=roleIdentifier,
            isDBFetch=isDBFetch,
        )
