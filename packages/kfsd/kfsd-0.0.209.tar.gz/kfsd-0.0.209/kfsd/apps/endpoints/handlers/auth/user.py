from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.auth.base import BasePermHandler
from kfsd.apps.endpoints.serializers.auth.user import (
    UserModelSerializer,
    UserSharedViewSerializer,
)
from kfsd.apps.models.tables.auth.user import User
from kfsd.apps.endpoints.handlers.auth.access import AccessHandler
from kfsd.apps.core.common.search import SearchQueries, SearchQuery
from kfsd.apps.endpoints.handlers.relations.base import handle_pre_del_process


def gen_user_handler(instance):
    handler = UserHandler(instance.identifier, False)
    qsData = UserModelSerializer(instance=instance)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=User)
def process_post_save(sender, instance, created, **kwargs):
    handler = gen_user_handler(instance)
    if not instance.policy:
        handler.setPolicy()


@receiver(pre_delete, sender=User)
def process_pre_del(sender, instance, **kwargs):
    handle_pre_del_process(instance)


class UserHandler(BasePermHandler):
    def __init__(self, userIdentifier, isDBFetch):
        BasePermHandler.__init__(
            self,
            serializer=UserModelSerializer,
            viewSerializer=UserSharedViewSerializer,
            modelClass=User,
            identifier=userIdentifier,
            isDBFetch=isDBFetch,
        )

    def genAccessResourceTypeQuery(self, resourceType, perm):
        filterQuery = SearchQuery(SearchQueries.ATTR_SEARCH_AND_KEY)
        filterQuery.add("actor__identifier", "str", [self.getIdentifier()])
        filterQuery.add("resource_type", "str", [resourceType])
        return SearchQueries.generate(SearchQueries.ATTR_SEARCH_AND_KEY, filterQuery)

    def filterResourcesByType(self, resourceType, perm):
        accessHandler = AccessHandler(None, False)
        accessQS = accessHandler.search(
            self.genAccessResourceTypeQuery(resourceType, perm).toFilterQueries()
        )
        return [qs.resource.identifier for qs in accessQS if perm in qs.permissions]
