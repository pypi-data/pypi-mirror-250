from rest_framework import serializers
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator,
)

from kfsd.apps.models.constants import MIN_LENGTH, MAX_LENGTH
from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.relations.hrel import HRel
from kfsd.apps.models.tables.auth.access import Access
from kfsd.apps.models.constants import ACTION_NAME_REGEX_CONDITION


class AccessResourcesFilterReq(serializers.Serializer):
    resource_type = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
        ]
    )
    action = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
            RegexValidator(
                ACTION_NAME_REGEX_CONDITION,
                message=(
                    "action name has to match {}".format(ACTION_NAME_REGEX_CONDITION)
                ),
                code="invalid_name",
            ),
        ]
    )


class AccessModelSerializer(BaseModelSerializer):
    actor = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=HRel.objects.all(),
    )
    actor_type = serializers.CharField(
        required=False,
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ],
    )
    resource = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=HRel.objects.all(),
    )
    resource_type = serializers.CharField(
        required=False,
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ],
    )
    permissions = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
        ],
    )

    class Meta:
        model = Access
        fields = "__all__"


class AccessViewModelSerializer(AccessModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Access
        exclude = ("created", "updated", "id")
