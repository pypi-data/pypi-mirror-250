from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.auth.docs.v1.apikey import APIKeyDocV1
from kfsd.apps.endpoints.serializers.auth.apikey import APIKeyViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class APIKeyDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**APIKeyDoc.modelviewset_list()),
            "retrieve": extend_schema(**APIKeyDoc.modelviewset_get()),
            "destroy": extend_schema(**APIKeyDoc.modelviewset_delete()),
            "partial_update": extend_schema(**APIKeyDoc.modelviewset_patch()),
            "create": extend_schema(**APIKeyDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "APIKey - Create",
            "description": "APIKey Create",
            "tags": ["MODELS : AUTH : APIKEY"],
            "responses": {
                200: APIKeyViewModelSerializer,
                409: ErrorSerializer,
                400: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": APIKeyDocV1.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "APIKey - Partial Update",
            "description": "APIKey Partial Update",
            "tags": ["MODELS : AUTH : APIKEY"],
            "responses": {
                200: APIKeyViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": APIKeyDocV1.modelviewset_patch_path_examples(),
            "examples": APIKeyDocV1.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "APIKey - Delete",
            "description": "APIKey Delete",
            "tags": ["MODELS : AUTH : APIKEY"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": APIKeyDocV1.modelviewset_delete_path_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "APIKey - List",
            "tags": ["MODELS : AUTH : APIKEY"],
            "responses": {
                200: APIKeyViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": APIKeyDocV1.modelviewset_list_path_examples(),
            "examples": APIKeyDocV1.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "APIKey - Get",
            "description": "APIKey Detail",
            "tags": ["MODELS : AUTH : APIKEY"],
            "responses": {
                200: APIKeyViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": APIKeyDocV1.modelviewset_get_path_examples(),
            "examples": APIKeyDocV1.modelviewset_get_examples(),
        }
