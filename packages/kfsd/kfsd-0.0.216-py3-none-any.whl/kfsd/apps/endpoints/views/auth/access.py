from drf_spectacular.utils import extend_schema_view

from kfsd.apps.models.tables.auth.access import Access
from kfsd.apps.endpoints.views.auth.docs.access import AccessDoc
from kfsd.apps.endpoints.serializers.auth.access import AccessViewModelSerializer
from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet


@extend_schema_view(**AccessDoc.modelviewset())
class AccessModelViewSet(CustomModelViewSet):
    queryset = Access.objects.all()
    serializer_class = AccessViewModelSerializer
