from django.urls import path, include
from rest_framework import routers

from kfsd.apps.endpoints.views.auth.user import UserModelViewSet
from kfsd.apps.endpoints.views.auth.team import TeamModelViewSet
from kfsd.apps.endpoints.views.auth.role import RoleModelViewSet
from kfsd.apps.endpoints.views.auth.org import OrgModelViewSet
from kfsd.apps.endpoints.views.auth.apikey import APIKeyModelViewSet
from kfsd.apps.endpoints.views.auth.access import AccessModelViewSet
from kfsd.apps.endpoints.views.auth.service import ServiceModelViewSet
from kfsd.apps.endpoints.views.auth.plan import PlanModelViewSet

router = routers.DefaultRouter()
router.include_format_suffixes = False

router.register("auth/user", UserModelViewSet, basename="user")
router.register("auth/team", TeamModelViewSet, basename="team")
router.register("auth/role", RoleModelViewSet, basename="role")
router.register("auth/org", OrgModelViewSet, basename="org")
router.register("auth/apikey", APIKeyModelViewSet, basename="apikey")
router.register("auth/access", AccessModelViewSet, basename="access")
router.register("auth/service", ServiceModelViewSet, basename="service")
router.register("auth/plan", PlanModelViewSet, basename="plan")

urlpatterns = [
    path("", include(router.urls)),
]
