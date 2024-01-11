from rest_framework import serializers

from kfsd.apps.endpoints.serializers.relations.hierarchy import (
    ChildrenViewSerializer,
    ParentViewSerializer,
)
from kfsd.apps.endpoints.serializers.relations.hrel import BaseHRelModelSerializer

from kfsd.apps.models.tables.auth.org import Org


class OrgModelSerializer(BaseHRelModelSerializer):
    type = serializers.CharField(read_only=True)
    attrs = serializers.JSONField(default=dict)
    policy = serializers.SlugRelatedField(
        required=False, many=False, read_only=True, slug_field="identifier"
    )

    class Meta:
        model = Org
        fields = "__all__"


class OrgViewModelSerializer(OrgModelSerializer):
    id = None
    created = None
    updated = None
    relations_from = None
    hierarchy_init = None
    children = ChildrenViewSerializer(many=True, read_only=True)
    parents = ParentViewSerializer(many=True, read_only=True)

    class Meta:
        model = Org
        exclude = ("created", "updated", "id")


class OrgSharedViewSerializer(OrgViewModelSerializer):
    class Meta:
        model = Org
        fields = ["identifier"]
