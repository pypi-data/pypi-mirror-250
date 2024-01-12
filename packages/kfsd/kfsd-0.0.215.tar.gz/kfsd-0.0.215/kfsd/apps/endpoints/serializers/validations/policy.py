from rest_framework import serializers
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.models.tables.validations.policy import Policy
from kfsd.apps.endpoints.serializers.validations.rule import RuleViewModelSerializer
from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH
from kfsd.apps.models.tables.general.data import Data


class PolicyModelSerializer(BaseModelSerializer):
    name = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ]
    )
    type = serializers.CharField(
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ]
    )
    resources = serializers.SlugRelatedField(
        required=False,
        many=True,
        read_only=False,
        slug_field="identifier",
        queryset=Data.objects.all(),
    )
    all_values = serializers.JSONField(default=list)
    rules = RuleViewModelSerializer(many=True, required=False)

    class Meta:
        model = Policy
        fields = "__all__"


class PolicyViewModelSerializer(PolicyModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Policy
        exclude = ("created", "updated", "id")
