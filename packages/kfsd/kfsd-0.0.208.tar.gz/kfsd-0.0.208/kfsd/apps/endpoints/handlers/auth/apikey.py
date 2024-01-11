from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.auth.base import BasePermHandler
from kfsd.apps.endpoints.serializers.auth.apikey import (
    APIKeyModelSerializer,
    APIKeySharedViewSerializer,
)
from kfsd.apps.models.tables.auth.apikey import APIKey
from kfsd.apps.endpoints.handlers.relations.base import handle_pre_del_process


def gen_apikey_handler(instance):
    handler = APIKeyHandler(instance.identifier, False)
    qsData = APIKeyModelSerializer(instance=instance)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=APIKey)
def process_post_save(sender, instance, created, **kwargs):
    handler = gen_apikey_handler(instance)
    if not instance.policy:
        handler.setPolicy()


@receiver(pre_delete, sender=APIKey)
def process_pre_del(sender, instance, **kwargs):
    handle_pre_del_process(instance)


class APIKeyHandler(BasePermHandler):
    def __init__(self, apiKeyIdentifier, isDBFetch):
        BasePermHandler.__init__(
            self,
            serializer=APIKeyModelSerializer,
            viewSerializer=APIKeySharedViewSerializer,
            modelClass=APIKey,
            identifier=apiKeyIdentifier,
            isDBFetch=isDBFetch,
        )
