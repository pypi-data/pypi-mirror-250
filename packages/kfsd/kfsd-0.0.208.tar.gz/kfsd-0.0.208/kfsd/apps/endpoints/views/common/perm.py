from rest_framework.response import Response
from rest_framework import status

from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.endpoints.views.common.model import ModelViewSet
from kfsd.apps.core.auth.token import TokenUser
from kfsd.apps.core.exceptions.api import KubefacetsAPIException
from kfsd.apps.core.common.kubefacets_config import KubefacetsConfig
from kfsd.apps.endpoints.handlers.relations.relation import (
    has_relation,
    add_relation,
    remove_relation,
)
from kfsd.apps.endpoints.handlers.relations.hrel import HRelHandler
from kfsd.apps.core.utils.system import System


class PermModelViewSet(ModelViewSet):
    ACCESS = "access"
    lookup_field = "identifier"
    lookup_value_regex = "[^/]+"

    def getModelName(self):
        return self.queryset.model._meta.verbose_name

    def isPermEnabled(self, request):
        if (
            self.request.token_user.isAuthEnabled()
            and self.request.token_user.isAuthenticated()
        ):
            return True
        return False

    def getUser(self, request) -> TokenUser:
        return self.request.token_user

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.isPermEnabled(self.request):
            user = self.getUser(self.request)
            resp = user.has_perm_all_resources("can_view", self.getModelName())
            return queryset.filter(identifier__in=resp)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if self.isPermEnabled(self.request):
            if not self.getUser(self.request).isAuthenticated():
                raise KubefacetsAPIException(
                    "Permission Denied",
                    "permission_denied",
                    status.HTTP_401_UNAUTHORIZED,
                )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.isPermEnabled(self.request):
            user = self.getUser(self.request)
            if not user.has_perm("can_edit", instance):
                raise KubefacetsAPIException(
                    "Permission Denied",
                    "permission_denied",
                    status.HTTP_401_UNAUTHORIZED,
                )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.isPermEnabled(self.request):
            user = self.getUser(self.request)
            if not user.has_perm("can_delete", instance):
                raise KubefacetsAPIException(
                    "Permission Denied",
                    "permission_denied",
                    status.HTTP_401_UNAUTHORIZED,
                )
        instance.delete()
        return Response({}, status.HTTP_204_NO_CONTENT)

    def getTeamAccessSerializer(self):
        return None

    def getUserAccessSerializer(self):
        return None

    def getAllowedPerms(self, permConfigKey):
        config = KubefacetsConfig().getConfig()
        serviceid = System.getEnv("service_id")
        configKey = "services.context.{}.allowed_perms.{}".format(
            serviceid, permConfigKey
        )
        return DictUtils.get_by_path(config, configKey)

    def parse_team_access_req(self, request, perm_config_key, identifier):
        serializer = self.getTeamAccessSerializer()(
            data=request.data,
            context={"allowed_perms": self.getAllowedPerms(perm_config_key)},
        )
        serializer.is_valid(raise_exception=True)
        sourceHandler = HRelHandler(serializer.data["team"], True)
        targetHandler = HRelHandler(identifier, True)
        perm = serializer.data["access"]
        return sourceHandler.getModelQS(), targetHandler.getModelQS(), perm

    def getSuccessResp(self):
        return Response({"status": "ok"}, status.HTTP_200_OK)

    def notFoundResp(self):
        return Response(
            {"detail": "relation not found", "code": "not_found"},
            status.HTTP_404_NOT_FOUND,
        )

    def add_access(self, source, target, perm):
        if has_relation(source, target, self.ACCESS, perm):
            return self.getSuccessResp()
        else:
            add_relation(source, target, self.ACCESS, perm)
            return self.getSuccessResp()

    def del_access(self, source, target, perm):
        if not has_relation(source, target, self.ACCESS, perm):
            return self.notFoundResp()
        else:
            remove_relation(source, target, self.ACCESS, perm)
            return self.getSuccessResp()

    def team_access_add(self, request, perm_config_key, identifier=None):
        source, target, perm = self.parse_team_access_req(
            request, perm_config_key, identifier
        )
        return self.add_access(source, target, perm)

    def team_access_del(self, request, perm_config_key, identifier=None):
        source, target, perm = self.parse_team_access_req(
            request, perm_config_key, identifier
        )
        return self.del_access(source, target, perm)

    def parse_user_access_req(self, request, perm_config_key, identifier):
        serializer = self.getUserAccessSerializer()(
            data=request.data,
            context={"allowed_perms": self.getAllowedPerms(perm_config_key)},
        )
        serializer.is_valid(raise_exception=True)

        sourceHandler = HRelHandler(serializer.data["user"], True)
        targetHandler = HRelHandler(identifier, True)
        perm = serializer.data["access"]
        return sourceHandler.getModelQS(), targetHandler.getModelQS(), perm

    def user_access_add(self, request, perm_config_key, identifier=None):
        source, target, perm = self.parse_user_access_req(
            request, perm_config_key, identifier
        )
        return self.add_access(source, target, perm)

    def user_access_del(self, request, perm_config_key, identifier=None):
        source, target, perm = self.parse_user_access_req(
            request, perm_config_key, identifier
        )
        return self.del_access(source, target, perm)
