from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.auth.plan import Plan
from kfsd.apps.endpoints.serializers.auth.plan import PlanViewModelSerializer
from kfsd.apps.endpoints.views.auth.docs.plan import PlanDoc


@extend_schema_view(**PlanDoc.modelviewset())
class PlanModelViewSet(CustomModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanViewModelSerializer
