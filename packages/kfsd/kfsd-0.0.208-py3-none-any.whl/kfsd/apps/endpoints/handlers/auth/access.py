from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.core.common.logger import Logger, LogLevel

from kfsd.apps.endpoints.serializers.auth.access import (
    AccessModelSerializer,
    AccessViewModelSerializer,
)
from kfsd.apps.models.tables.auth.access import Access, gen_access_id

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


def gen_access_handler(instance):
    handler = AccessHandler(instance.identifier, False)
    qsData = AccessModelSerializer(instance=instance)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


def add_access(perms, actor, resource):
    accessId = gen_access_id(actor, resource)
    accessHandler = AccessHandler(accessId, False)
    if not accessHandler.exists():
        if len(perms) > 0:
            Access.objects.create(permissions=perms, actor=actor, resource=resource)
    else:
        instance = Access.objects.get(actor=actor, resource=resource)
        if instance.permissions != perms:
            if len(perms) > 0:
                instance.permissions = perms
                instance.save()
            else:
                instance.delete()


def rm_all_access(actor, resource):
    accessQS = Access.objects.filter(actor=actor, resource=resource)
    if accessQS:
        accessQS.delete()


class AccessHandler(BaseHandler):
    def __init__(self, accessIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=AccessModelSerializer,
            viewSerializer=AccessViewModelSerializer,
            modelClass=Access,
            identifier=accessIdentifier,
            isDBFetch=isDBFetch,
        )

    def search(self, queries):
        return Access.objects.filter(queries)
