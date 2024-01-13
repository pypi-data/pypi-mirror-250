from rest_framework import serializers

from kfsd.apps.endpoints.serializers.relations.hierarchy import (
    ChildrenViewSerializer,
    ParentViewSerializer,
)
from kfsd.apps.endpoints.serializers.relations.hrel import BaseHRelModelSerializer

from kfsd.apps.models.tables.auth.service import Service


class ServiceModelSerializer(BaseHRelModelSerializer):
    type = serializers.CharField(read_only=True)
    attrs = serializers.JSONField(default=dict)
    policy = serializers.SlugRelatedField(
        required=False, many=False, read_only=True, slug_field="identifier"
    )

    class Meta:
        model = Service
        fields = "__all__"


class ServiceViewModelSerializer(ServiceModelSerializer):
    id = None
    created = None
    updated = None
    relations_from = None
    hierarchy_init = None
    children = ChildrenViewSerializer(many=True, read_only=True)
    parents = ParentViewSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        exclude = ("created", "updated", "id")


class ServiceSharedViewSerializer(ServiceViewModelSerializer):
    class Meta:
        model = Service
        fields = ["identifier"]
