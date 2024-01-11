from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class APIKeyDocV1:
    @staticmethod
    def modelviewset_list_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.QUERY,
                name="page",
                required=False,
                type=OpenApiTypes.INT,
                examples=[
                    OpenApiExample("Example 1", summary="Pagination", value=1),
                    OpenApiExample("Example 2", summary="Pagination", value=2),
                ],
            )
        ]

    @staticmethod
    def modelviewset_list_examples():
        return [
            OpenApiExample(
                "APIKey - List All",
                value=[
                    {
                        "identifier": "AKE=be4f8cd203",
                        "type": "APIKey",
                        "relations": [],
                        "children": [],
                        "parents": [],
                        "parent": None,
                        "created_by": None,
                        "is_public": False,
                        "attrs": {
                            "identifier": "AKE=be4f8cd203",
                            "name": "Default",
                            "key": "1955466b4433bd74dbfae4bdf6b47419",
                            "slug": "default",
                            "assigned_to": "USR=bc389855ad",
                            "created_by": "USR=bc389855ad",
                            "desc": "Default api key for User",
                        },
                        "policy": "POLICY_TYPE=Resource,POLICY_NAME=APIKey",
                    }
                ],
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_get_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "APIKey - Get",
                        summary="APIKey Identifier",
                        description="APIKey - Get",
                        value="AKE=be4f8cd203",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "APIKey - Get",
                value={
                    "identifier": "AKE=be4f8cd203",
                    "type": "APIKey",
                    "relations": [],
                    "children": [],
                    "parents": [],
                    "parent": None,
                    "created_by": None,
                    "is_public": False,
                    "attrs": {
                        "identifier": "AKE=be4f8cd203",
                        "name": "Default",
                        "key": "1955466b4433bd74dbfae4bdf6b47419",
                        "slug": "default",
                        "assigned_to": "USR=bc389855ad",
                        "created_by": "USR=bc389855ad",
                        "desc": "Default api key for User",
                    },
                    "policy": "POLICY_TYPE=Resource,POLICY_NAME=APIKey",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "APIKey - Create",
                value={
                    "identifier": "AKE=be4f8cd203",
                    "is_public": False,
                    "attrs": {
                        "identifier": "AKE=be4f8cd203",
                        "name": "Default",
                        "key": "1955466b4433bd74dbfae4bdf6b47419",
                        "slug": "default",
                        "assigned_to": "USR=bc389855ad",
                        "created_by": "USR=bc389855ad",
                        "desc": "Default api key for User",
                    },
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "APIKey - Create",
                value={
                    "identifier": "AKE=be4f8cd203",
                    "type": "APIKey",
                    "relations": [],
                    "children": [],
                    "parents": [],
                    "parent": None,
                    "created_by": None,
                    "is_public": False,
                    "attrs": {
                        "identifier": "AKE=be4f8cd203",
                        "name": "Default",
                        "key": "1955466b4433bd74dbfae4bdf6b47419",
                        "slug": "default",
                        "assigned_to": "USR=bc389855ad",
                        "created_by": "USR=bc389855ad",
                        "desc": "Default api key for User",
                    },
                    "policy": "POLICY_TYPE=Resource,POLICY_NAME=APIKey",
                },
                request_only=False,
                response_only=True,
            ),
        ]

    @staticmethod
    def modelviewset_delete_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "APIKey - Delete",
                        summary="APIKey Identifier",
                        value="AKE=be4f8cd203",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "APIKey - Patch",
                        summary="APIKey Identifier",
                        description="APIKey - Patch",
                        value="AKE=be4f8cd203",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "APIKey - Patch",
                value={
                    "attrs": {
                        "identifier": "AKE=be4f8cd203",
                        "name": "Default",
                        "key": "1955466b4433bd74dbfae4bdf6b47419",
                        "slug": "default",
                        "assigned_to": "USR=bc389855ad",
                        "created_by": "USR=bc389855ad",
                        "desc": "Default api key for User",
                    }
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "APIKey - Patch",
                value={
                    "identifier": "AKE=be4f8cd203",
                    "type": "APIKey",
                    "relations": [],
                    "children": [],
                    "parents": [],
                    "parent": None,
                    "created_by": None,
                    "is_public": False,
                    "attrs": {
                        "identifier": "AKE=be4f8cd203",
                        "name": "Default",
                        "key": "1955466b4433bd74dbfae4bdf6b47419",
                        "slug": "default",
                        "assigned_to": "USR=bc389855ad",
                        "created_by": "USR=bc389855ad",
                        "desc": "Default api key for User",
                    },
                    "policy": "POLICY_TYPE=Resource,POLICY_NAME=APIKey",
                },
                request_only=False,
                response_only=True,
            ),
        ]
