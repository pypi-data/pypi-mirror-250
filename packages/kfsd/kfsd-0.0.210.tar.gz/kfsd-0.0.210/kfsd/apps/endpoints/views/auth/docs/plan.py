from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.auth.docs.v1.plan import PlanDocV1
from kfsd.apps.endpoints.serializers.auth.plan import PlanViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class PlanDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**PlanDoc.modelviewset_list()),
            "retrieve": extend_schema(**PlanDoc.modelviewset_get()),
            "destroy": extend_schema(**PlanDoc.modelviewset_delete()),
            "partial_update": extend_schema(**PlanDoc.modelviewset_patch()),
            "create": extend_schema(**PlanDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Plan - Create",
            "description": "Plan Create",
            "tags": ["MODELS : AUTH : PLAN"],
            "responses": {
                200: PlanViewModelSerializer,
                409: ErrorSerializer,
                400: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": PlanDocV1.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Plan - Partial Update",
            "description": "Plan Partial Update",
            "tags": ["MODELS : AUTH : PLAN"],
            "responses": {
                200: PlanViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": PlanDocV1.modelviewset_patch_path_examples(),
            "examples": PlanDocV1.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Plan - Delete",
            "description": "Plan Delete",
            "tags": ["MODELS : AUTH : PLAN"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": PlanDocV1.modelviewset_delete_path_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Plan - List",
            "tags": ["MODELS : AUTH : PLAN"],
            "responses": {
                200: PlanViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": PlanDocV1.modelviewset_list_path_examples(),
            "examples": PlanDocV1.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Plan - Get",
            "description": "Plan Detail",
            "tags": ["MODELS : AUTH : PLAN"],
            "responses": {
                200: PlanViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": PlanDocV1.modelviewset_get_path_examples(),
            "examples": PlanDocV1.modelviewset_get_examples(),
        }
