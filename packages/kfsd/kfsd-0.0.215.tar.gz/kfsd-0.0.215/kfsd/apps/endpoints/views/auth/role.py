from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.auth.role import Role
from kfsd.apps.endpoints.serializers.auth.role import RoleViewModelSerializer
from kfsd.apps.endpoints.views.auth.docs.role import RoleDoc


@extend_schema_view(**RoleDoc.modelviewset())
class RoleModelViewSet(CustomModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleViewModelSerializer
