from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiTypes

from kfsd.apps.endpoints.views.auth.docs.v1.user import UserDocV1
from kfsd.apps.endpoints.serializers.auth.user import UserViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
    SuccessSerializer,
)
from kfsd.apps.endpoints.serializers.auth.access import AccessResourcesFilterReq


class UserDoc:
    @staticmethod
    def filter_resources_view():
        return {
            "summary": "User - Filter Resources",
            "description": "User Filter Resources",
            "tags": ["MODELS : AUTH : USER"],
            "request": AccessResourcesFilterReq,
            "responses": {
                200: OpenApiTypes.ANY,
                409: ErrorSerializer,
                400: ErrorSerializer,
                500: ErrorSerializer,
            },
            "parameters": UserDocV1.modelviewset_patch_path_examples(),
            "examples": UserDocV1.filter_resources_view_examples(),
        }

    @staticmethod
    def update_access_view():
        return {
            "summary": "User - Update Access",
            "description": "User Update Access",
            "tags": ["MODELS : AUTH : USER"],
            "responses": {
                200: SuccessSerializer,
                409: ErrorSerializer,
                400: ErrorSerializer,
                500: ErrorSerializer,
            },
        }

    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**UserDoc.modelviewset_list()),
            "retrieve": extend_schema(**UserDoc.modelviewset_get()),
            "destroy": extend_schema(**UserDoc.modelviewset_delete()),
            "partial_update": extend_schema(**UserDoc.modelviewset_patch()),
            "create": extend_schema(**UserDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "User - Create",
            "description": "User Create",
            "tags": ["MODELS : AUTH : USER"],
            "responses": {
                200: UserViewModelSerializer,
                409: ErrorSerializer,
                400: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": UserDocV1.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "User - Partial Update",
            "description": "User Partial Update",
            "tags": ["MODELS : AUTH : USER"],
            "responses": {
                200: UserViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": UserDocV1.modelviewset_patch_path_examples(),
            "examples": UserDocV1.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "User - Delete",
            "description": "User Delete",
            "tags": ["MODELS : AUTH : USER"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": UserDocV1.modelviewset_delete_path_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "User - List",
            "tags": ["MODELS : AUTH : USER"],
            "responses": {
                200: UserViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": UserDocV1.modelviewset_list_path_examples(),
            "examples": UserDocV1.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "User - Get",
            "description": "User Detail",
            "tags": ["MODELS : AUTH : USER"],
            "responses": {
                200: UserViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": UserDocV1.modelviewset_get_path_examples(),
            "examples": UserDocV1.modelviewset_get_examples(),
        }
