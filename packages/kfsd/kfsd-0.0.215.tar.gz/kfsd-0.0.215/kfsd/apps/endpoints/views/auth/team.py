from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.auth.team import Team
from kfsd.apps.endpoints.serializers.auth.team import TeamViewModelSerializer
from kfsd.apps.endpoints.views.auth.docs.team import TeamDoc


@extend_schema_view(**TeamDoc.modelviewset())
class TeamModelViewSet(CustomModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamViewModelSerializer
