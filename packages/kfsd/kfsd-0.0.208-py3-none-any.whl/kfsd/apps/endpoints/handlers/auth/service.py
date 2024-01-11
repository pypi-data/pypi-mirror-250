from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.auth.base import BasePermHandler
from kfsd.apps.endpoints.serializers.auth.service import (
    ServiceModelSerializer,
    ServiceSharedViewSerializer,
)
from kfsd.apps.models.tables.auth.service import Service
from kfsd.apps.endpoints.handlers.relations.base import handle_pre_del_process


def gen_service_handler(instance):
    handler = ServiceHandler(instance.identifier, False)
    qsData = ServiceModelSerializer(instance=instance)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Service)
def process_post_save(sender, instance, created, **kwargs):
    handler = gen_service_handler(instance)
    if not instance.policy:
        handler.setPolicy()


@receiver(pre_delete, sender=Service)
def process_pre_del(sender, instance, **kwargs):
    handle_pre_del_process(instance)


class ServiceHandler(BasePermHandler):
    def __init__(self, serviceIdentifier, isDBFetch):
        BasePermHandler.__init__(
            self,
            serializer=ServiceModelSerializer,
            viewSerializer=ServiceSharedViewSerializer,
            modelClass=Service,
            identifier=serviceIdentifier,
            isDBFetch=isDBFetch,
        )
