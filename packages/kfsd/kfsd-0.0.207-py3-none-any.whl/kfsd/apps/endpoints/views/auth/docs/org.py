from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.auth.docs.v1.org import OrgDocV1
from kfsd.apps.endpoints.serializers.auth.org import OrgViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class OrgDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**OrgDoc.modelviewset_list()),
            "retrieve": extend_schema(**OrgDoc.modelviewset_get()),
            "destroy": extend_schema(**OrgDoc.modelviewset_delete()),
            "partial_update": extend_schema(**OrgDoc.modelviewset_patch()),
            "create": extend_schema(**OrgDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Org - Create",
            "description": "Org Create",
            "tags": ["MODELS : AUTH : ORG"],
            "responses": {
                200: OrgViewModelSerializer,
                409: ErrorSerializer,
                400: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": OrgDocV1.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Org - Partial Update",
            "description": "Org Partial Update",
            "tags": ["MODELS : AUTH : ORG"],
            "responses": {
                200: OrgViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": OrgDocV1.modelviewset_patch_path_examples(),
            "examples": OrgDocV1.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Org - Delete",
            "description": "Org Delete",
            "tags": ["MODELS : AUTH : ORG"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": OrgDocV1.modelviewset_delete_path_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Org - List",
            "tags": ["MODELS : AUTH : ORG"],
            "responses": {
                200: OrgViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": OrgDocV1.modelviewset_list_path_examples(),
            "examples": OrgDocV1.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Org - Get",
            "description": "Org Detail",
            "tags": ["MODELS : AUTH : ORG"],
            "responses": {
                200: OrgViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": OrgDocV1.modelviewset_get_path_examples(),
            "examples": OrgDocV1.modelviewset_get_examples(),
        }
