from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.auth.docs.v1.service import ServiceDocV1
from kfsd.apps.endpoints.serializers.auth.service import ServiceViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class ServiceDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**ServiceDoc.modelviewset_list()),
            "retrieve": extend_schema(**ServiceDoc.modelviewset_get()),
            "destroy": extend_schema(**ServiceDoc.modelviewset_delete()),
            "partial_update": extend_schema(**ServiceDoc.modelviewset_patch()),
            "create": extend_schema(**ServiceDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Service - Create",
            "description": "Service Create",
            "tags": ["MODELS : AUTH : SERVICE"],
            "responses": {
                200: ServiceViewModelSerializer,
                409: ErrorSerializer,
                400: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": ServiceDocV1.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Service - Partial Update",
            "description": "Service Partial Update",
            "tags": ["MODELS : AUTH : SERVICE"],
            "responses": {
                200: ServiceViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ServiceDocV1.modelviewset_patch_path_examples(),
            "examples": ServiceDocV1.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Service - Delete",
            "description": "Service Delete",
            "tags": ["MODELS : AUTH : SERVICE"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": ServiceDocV1.modelviewset_delete_path_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Service - List",
            "tags": ["MODELS : AUTH : SERVICE"],
            "responses": {
                200: ServiceViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ServiceDocV1.modelviewset_list_path_examples(),
            "examples": ServiceDocV1.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Service - Get",
            "description": "Service Detail",
            "tags": ["MODELS : AUTH : SERVICE"],
            "responses": {
                200: ServiceViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": ServiceDocV1.modelviewset_get_path_examples(),
            "examples": ServiceDocV1.modelviewset_get_examples(),
        }
