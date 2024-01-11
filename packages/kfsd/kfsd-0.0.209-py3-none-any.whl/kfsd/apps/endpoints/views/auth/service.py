from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.auth.service import Service
from kfsd.apps.endpoints.serializers.auth.service import ServiceViewModelSerializer
from kfsd.apps.endpoints.views.auth.docs.service import ServiceDoc


@extend_schema_view(**ServiceDoc.modelviewset())
class ServiceModelViewSet(CustomModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceViewModelSerializer
