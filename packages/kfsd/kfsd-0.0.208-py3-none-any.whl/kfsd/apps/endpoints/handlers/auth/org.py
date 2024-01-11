from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.auth.base import BasePermHandler
from kfsd.apps.endpoints.serializers.auth.org import (
    OrgModelSerializer,
    OrgSharedViewSerializer,
)
from kfsd.apps.models.tables.auth.org import Org
from kfsd.apps.endpoints.handlers.relations.base import handle_pre_del_process


def gen_org_handler(instance):
    handler = OrgHandler(instance.identifier, False)
    qsData = OrgModelSerializer(instance=instance)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Org)
def process_post_save(sender, instance, created, **kwargs):
    handler = gen_org_handler(instance)
    if not instance.policy:
        handler.setPolicy()


@receiver(pre_delete, sender=Org)
def process_pre_del(sender, instance, **kwargs):
    handle_pre_del_process(instance)


class OrgHandler(BasePermHandler):
    def __init__(self, orgIdentifier, isDBFetch):
        BasePermHandler.__init__(
            self,
            serializer=OrgModelSerializer,
            viewSerializer=OrgSharedViewSerializer,
            modelClass=Org,
            identifier=orgIdentifier,
            isDBFetch=isDBFetch,
        )
