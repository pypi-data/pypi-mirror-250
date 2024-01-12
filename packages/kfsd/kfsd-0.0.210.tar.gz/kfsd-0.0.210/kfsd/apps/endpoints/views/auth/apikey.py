from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.auth.apikey import APIKey
from kfsd.apps.endpoints.serializers.auth.apikey import APIKeyViewModelSerializer
from kfsd.apps.endpoints.views.auth.docs.apikey import APIKeyDoc


@extend_schema_view(**APIKeyDoc.modelviewset())
class APIKeyModelViewSet(CustomModelViewSet):
    queryset = APIKey.objects.all()
    serializer_class = APIKeyViewModelSerializer
