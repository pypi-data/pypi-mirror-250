from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.auth.user import User
from kfsd.apps.endpoints.serializers.auth.user import UserViewModelSerializer
from kfsd.apps.endpoints.views.auth.docs.user import UserDoc
from kfsd.apps.endpoints.handlers.auth.user import UserHandler
from kfsd.apps.endpoints.serializers.auth.access import AccessResourcesFilterReq


@extend_schema_view(**UserDoc.modelviewset())
class UserModelViewSet(CustomModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserViewModelSerializer

    def filterResources(self, request, identifier):
        serializer = AccessResourcesFilterReq(data=request.data)
        if serializer.is_valid(raise_exception=True):
            userHandler = UserHandler(identifier, True)
            return userHandler.filterResourcesByType(
                serializer.data["resource_type"], serializer.data["action"]
            )

    @extend_schema(**UserDoc.filter_resources_view())
    @action(
        detail=True,
        methods=["post"],
        renderer_classes=[JSONRenderer],
        url_path="access/filter",
    )
    def filter_resources(self, request, identifier=None):
        ids = self.filterResources(request, identifier)
        return Response(ids, status.HTTP_200_OK)
