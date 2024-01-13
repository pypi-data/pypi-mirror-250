from rest_framework import serializers

from kfsd.apps.endpoints.serializers.relations.hierarchy import (
    ChildrenViewSerializer,
    ParentViewSerializer,
)
from kfsd.apps.endpoints.serializers.relations.hrel import BaseHRelModelSerializer

from kfsd.apps.models.tables.auth.apikey import APIKey


class APIKeyModelSerializer(BaseHRelModelSerializer):
    type = serializers.CharField(read_only=True)
    attrs = serializers.JSONField(default=dict)
    policy = serializers.SlugRelatedField(
        required=False, many=False, read_only=True, slug_field="identifier"
    )

    class Meta:
        model = APIKey
        fields = "__all__"


class APIKeyViewModelSerializer(APIKeyModelSerializer):
    id = None
    created = None
    updated = None
    relations_from = None
    hierarchy_init = None
    children = ChildrenViewSerializer(many=True, read_only=True)
    parents = ParentViewSerializer(many=True, read_only=True)

    class Meta:
        model = APIKey
        exclude = ("created", "updated", "id")


class APIKeySharedViewSerializer(APIKeyViewModelSerializer):
    class Meta:
        model = APIKey
        fields = ["identifier"]
