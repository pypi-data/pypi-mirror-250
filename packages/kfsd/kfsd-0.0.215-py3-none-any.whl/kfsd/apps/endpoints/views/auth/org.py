from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.auth.org import Org
from kfsd.apps.endpoints.serializers.auth.org import OrgViewModelSerializer
from kfsd.apps.endpoints.views.auth.docs.org import OrgDoc


@extend_schema_view(**OrgDoc.modelviewset())
class OrgModelViewSet(CustomModelViewSet):
    queryset = Org.objects.all()
    serializer_class = OrgViewModelSerializer
