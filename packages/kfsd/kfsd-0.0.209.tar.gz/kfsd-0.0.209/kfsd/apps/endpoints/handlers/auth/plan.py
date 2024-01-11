from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.auth.base import BasePermHandler
from kfsd.apps.endpoints.serializers.auth.plan import (
    PlanModelSerializer,
    PlanSharedViewSerializer,
)
from kfsd.apps.models.tables.auth.plan import Plan
from kfsd.apps.endpoints.handlers.relations.base import handle_pre_del_process


def gen_plan_handler(instance):
    handler = PlanHandler(instance.identifier, False)
    qsData = PlanModelSerializer(instance=instance)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Plan)
def process_post_save(sender, instance, created, **kwargs):
    handler = gen_plan_handler(instance)
    if not instance.policy:
        handler.setPolicy()


@receiver(pre_delete, sender=Plan)
def process_pre_del(sender, instance, **kwargs):
    handle_pre_del_process(instance)


class PlanHandler(BasePermHandler):
    def __init__(self, planIdentifier, isDBFetch):
        BasePermHandler.__init__(
            self,
            serializer=PlanModelSerializer,
            viewSerializer=PlanSharedViewSerializer,
            modelClass=Plan,
            identifier=planIdentifier,
            isDBFetch=isDBFetch,
        )
