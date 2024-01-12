from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.auth.docs.v1.team import TeamDocV1
from kfsd.apps.endpoints.serializers.auth.team import TeamViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class TeamDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**TeamDoc.modelviewset_list()),
            "retrieve": extend_schema(**TeamDoc.modelviewset_get()),
            "destroy": extend_schema(**TeamDoc.modelviewset_delete()),
            "partial_update": extend_schema(**TeamDoc.modelviewset_patch()),
            "create": extend_schema(**TeamDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "Team - Create",
            "description": "Team Create",
            "tags": ["MODELS : AUTH : TEAM"],
            "responses": {
                200: TeamViewModelSerializer,
                409: ErrorSerializer,
                400: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": TeamDocV1.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "Team - Partial Update",
            "description": "Team Partial Update",
            "tags": ["MODELS : AUTH : TEAM"],
            "responses": {
                200: TeamViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": TeamDocV1.modelviewset_patch_path_examples(),
            "examples": TeamDocV1.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "Team - Delete",
            "description": "Team Delete",
            "tags": ["MODELS : AUTH : TEAM"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": TeamDocV1.modelviewset_delete_path_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "Team - List",
            "tags": ["MODELS : AUTH : TEAM"],
            "responses": {
                200: TeamViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": TeamDocV1.modelviewset_list_path_examples(),
            "examples": TeamDocV1.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "Team - Get",
            "description": "Team Detail",
            "tags": ["MODELS : AUTH : TEAM"],
            "responses": {
                200: TeamViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": TeamDocV1.modelviewset_get_path_examples(),
            "examples": TeamDocV1.modelviewset_get_examples(),
        }
