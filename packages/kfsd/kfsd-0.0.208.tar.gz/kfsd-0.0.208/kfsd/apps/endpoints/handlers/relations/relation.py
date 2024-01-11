from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.relations.relation import (
    RelationViewModelSerializer,
)
from kfsd.apps.endpoints.handlers.signals.outbound import upsert_tbl_event
from kfsd.apps.models.tables.relations.relation import Relation


def gen_relation_handler(instance):
    handler = RelationHandler(instance.identifier, False)
    qsData = RelationViewModelSerializer(instance=instance)
    handler.setModelQSRawData(qsData)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


def rm_all_relations(instance):
    Relation.objects.filter(target=instance).delete()
    Relation.objects.filter(source=instance).delete()


def add_relation(source, target, name, val):
    Relation.objects.create(name=name, value=val, source=source, target=target)


def remove_relation(source, target, name, val):
    Relation.objects.filter(name=name, value=val, source=source, target=target).delete()


def has_relation(source, target, name, val):
    qs = Relation.objects.filter(name=name, value=val, source=source, target=target)
    return qs


@receiver(post_save, sender=Relation)
@upsert_tbl_event(gen_relation_handler)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Relation)
@upsert_tbl_event(gen_relation_handler)
def process_post_del(sender, instance, **kwargs):
    pass


class RelationHandler(BaseHandler):
    def __init__(self, hierarchyIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=RelationViewModelSerializer,
            viewSerializer=RelationViewModelSerializer,
            modelClass=Relation,
            identifier=hierarchyIdentifier,
            isDBFetch=isDBFetch,
        )
