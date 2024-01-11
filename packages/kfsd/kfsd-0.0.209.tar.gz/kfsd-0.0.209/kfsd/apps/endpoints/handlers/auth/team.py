from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.auth.base import BasePermHandler
from kfsd.apps.endpoints.serializers.auth.team import (
    TeamModelSerializer,
    TeamSharedViewSerializer,
)
from kfsd.apps.models.tables.auth.team import Team
from kfsd.apps.endpoints.handlers.relations.base import handle_pre_del_process


def gen_team_handler(instance):
    handler = TeamHandler(instance.identifier, False)
    qsData = TeamModelSerializer(instance=instance)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Team)
def process_post_save(sender, instance, created, **kwargs):
    handler = gen_team_handler(instance)
    if not instance.policy:
        handler.setPolicy()


@receiver(pre_delete, sender=Team)
def process_pre_del(sender, instance, **kwargs):
    handle_pre_del_process(instance)


class TeamHandler(BasePermHandler):
    def __init__(self, teamIdentifier, isDBFetch):
        BasePermHandler.__init__(
            self,
            serializer=TeamModelSerializer,
            viewSerializer=TeamSharedViewSerializer,
            modelClass=Team,
            identifier=teamIdentifier,
            isDBFetch=isDBFetch,
        )
