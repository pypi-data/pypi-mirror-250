from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.auth.docs.v1.role import RoleDocV1
from kfsd.apps.endpoints.serializers.auth.role import RoleViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class RoleDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**RoleDoc.modelviewset_list()),
            "retrieve": extend_schema(**RoleDoc.modelviewset_get()),
            "destroy": extend_schema(**RoleDoc.modelviewset_delete()),
            "partial_update": extend_schema(**RoleDoc.modelviewset_patch()),
            "create": extend_schema(**RoleDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Role - Create",
            "description": "Role Create",
            "tags": ["MODELS : AUTH : ROLE"],
            "responses": {
                200: RoleViewModelSerializer,
                409: ErrorSerializer,
                400: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": RoleDocV1.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Role - Partial Update",
            "description": "Role Partial Update",
            "tags": ["MODELS : AUTH : ROLE"],
            "responses": {
                200: RoleViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": RoleDocV1.modelviewset_patch_path_examples(),
            "examples": RoleDocV1.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Role - Delete",
            "description": "Role Delete",
            "tags": ["MODELS : AUTH : ROLE"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": RoleDocV1.modelviewset_delete_path_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Role - List",
            "tags": ["MODELS : AUTH : ROLE"],
            "responses": {
                200: RoleViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": RoleDocV1.modelviewset_list_path_examples(),
            "examples": RoleDocV1.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Role - Get",
            "description": "Role Detail",
            "tags": ["MODELS : AUTH : ROLE"],
            "responses": {
                200: RoleViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": RoleDocV1.modelviewset_get_path_examples(),
            "examples": RoleDocV1.modelviewset_get_examples(),
        }
