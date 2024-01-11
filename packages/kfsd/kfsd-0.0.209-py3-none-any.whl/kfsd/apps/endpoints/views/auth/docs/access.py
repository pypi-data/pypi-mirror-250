from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.auth.docs.v1.access import AccessDocV1
from kfsd.apps.endpoints.serializers.auth.access import AccessViewModelSerializer
from kfsd.apps.endpoints.serializers.base import NotFoundSerializer, ErrorSerializer


class AccessDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**AccessDoc.modelviewset_list()),
            "retrieve": extend_schema(**AccessDoc.modelviewset_get()),
            "destroy": extend_schema(**AccessDoc.modelviewset_delete()),
            "partial_update": extend_schema(**AccessDoc.modelviewset_partial_update()),
            "create": extend_schema(**AccessDoc.modelviewset_create()),
        }

    def modelviewset_create():
        return {
            "summary": "Access - Create",
            "description": "Access Create",
            "tags": ["MODELS : AUTH : ACCESS"],
            "responses": {
                200: AccessViewModelSerializer,
                400: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": AccessDocV1.modelviewset_create_examples(),
        }

    def modelviewset_list():
        return {
            "summary": "Access - List",
            "description": "Data for different actors and resources",
            "tags": ["MODELS : AUTH : ACCESS"],
            "responses": {
                200: AccessViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": AccessDocV1.modelviewset_list_path_examples(),
            "examples": AccessDocV1.modelviewset_list_examples(),
        }

    def modelviewset_get():
        return {
            "summary": "Access - Get",
            "description": "Access Detail",
            "tags": ["MODELS : AUTH : ACCESS"],
            "responses": {
                200: AccessViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": AccessDocV1.modelviewset_get_path_examples(),
            "examples": AccessDocV1.modelviewset_get_examples(),
        }

    def modelviewset_delete():
        return {
            "summary": "Access - Delete",
            "description": "Access Delete",
            "tags": ["MODELS : AUTH : ACCESS"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": AccessDocV1.modelviewset_delete_path_examples(),
        }

    def modelviewset_partial_update():
        return {
            "summary": "Access - Partial Update",
            "description": "Access Patial Update",
            "tags": ["MODELS : AUTH : ACCESS"],
            "responses": {
                200: AccessViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": AccessDocV1.modelviewset_partial_update_path_examples(),
            "examples": AccessDocV1.modelviewset_partial_update_examples(),
        }
