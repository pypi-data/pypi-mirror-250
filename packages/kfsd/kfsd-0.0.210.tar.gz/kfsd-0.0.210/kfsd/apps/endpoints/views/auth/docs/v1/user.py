from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class UserDocV1:
    @staticmethod
    def filter_resources_view_examples():
        return [
            OpenApiExample(
                "User - Filter Resources",
                value={"resource_type": "User", "action": "view_user"},
                request_only=True,
                response_only=False,
            ),
        ]

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
                "User - List All",
                value=[
                    {
                        "identifier": "USR=bc389855ad",
                        "type": "User",
                        "relations": [
                            {
                                "identifier": "NAME=role,VALUE=owner,SOURCE=USR=bc389855ad,TARGET=AKE=be4f8cd203",
                                "target": "AKE=be4f8cd203",
                                "target_type": "APIKey",
                                "source": "USR=bc389855ad",
                                "source_type": "User",
                                "name": "role",
                                "value": "owner",
                            },
                            {
                                "identifier": "NAME=role,VALUE=member,SOURCE=USR=bc389855ad,TARGET=RLE=dbac701c35",
                                "target": "RLE=dbac701c35",
                                "target_type": "Role",
                                "source": "USR=bc389855ad",
                                "source_type": "User",
                                "name": "role",
                                "value": "member",
                            },
                        ],
                        "children": [],
                        "parents": [],
                        "parent": None,
                        "created_by": None,
                        "is_public": False,
                        "attrs": {
                            "identifier": "USR=bc389855ad",
                            "first_name": "Gokul Nathan",
                            "middle_name": "",
                            "last_name": "Chandran",
                            "username": "gokul",
                            "type": "User",
                            "is_staff": False,
                            "is_superuser": False,
                            "is_active": True,
                            "is_email_verified": True,
                            "email": "gokul@kubefacets.com",
                        },
                        "policy": "POLICY_TYPE=Resource,POLICY_NAME=User",
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
                        "User - Get",
                        summary="User Identifier",
                        description="User - Get",
                        value="USR=bc389855ad",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "User - Get",
                value={
                    "identifier": "USR=bc389855ad",
                    "type": "User",
                    "relations": [
                        {
                            "identifier": "NAME=role,VALUE=owner,SOURCE=USR=bc389855ad,TARGET=AKE=be4f8cd203",
                            "target": "AKE=be4f8cd203",
                            "target_type": "APIKey",
                            "source": "USR=bc389855ad",
                            "source_type": "User",
                            "name": "role",
                            "value": "owner",
                        },
                        {
                            "identifier": "NAME=role,VALUE=member,SOURCE=USR=bc389855ad,TARGET=RLE=dbac701c35",
                            "target": "RLE=dbac701c35",
                            "target_type": "Role",
                            "source": "USR=bc389855ad",
                            "source_type": "User",
                            "name": "role",
                            "value": "member",
                        },
                    ],
                    "children": [],
                    "parents": [],
                    "parent": None,
                    "created_by": None,
                    "is_public": False,
                    "attrs": {
                        "identifier": "USR=bc389855ad",
                        "first_name": "Gokul Nathan",
                        "middle_name": "",
                        "last_name": "Chandran",
                        "username": "gokul",
                        "type": "User",
                        "is_staff": False,
                        "is_superuser": False,
                        "is_active": True,
                        "is_email_verified": True,
                        "email": "gokul@kubefacets.com",
                    },
                    "policy": "POLICY_TYPE=Resource,POLICY_NAME=User",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "User - Create",
                value={
                    "identifier": "USR=bc389855ad",
                    "attrs": {
                        "identifier": "USR=bc389855ad",
                        "first_name": "Gokul Nathan",
                        "middle_name": "",
                        "last_name": "Chandran",
                        "username": "gokul",
                        "type": "User",
                        "is_staff": False,
                        "is_superuser": False,
                        "is_active": True,
                        "is_email_verified": True,
                        "email": "gokul@kubefacets.com",
                    },
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "User - Create",
                value={
                    "identifier": "USR=bc389855ad",
                    "type": "User",
                    "relations": [],
                    "children": [],
                    "parents": [],
                    "parent": None,
                    "created_by": None,
                    "is_public": False,
                    "attrs": {
                        "identifier": "USR=bc389855ad",
                        "first_name": "Gokul Nathan",
                        "middle_name": "",
                        "last_name": "Chandran",
                        "username": "gokul",
                        "type": "User",
                        "is_staff": False,
                        "is_superuser": False,
                        "is_active": True,
                        "is_email_verified": True,
                        "email": "gokul@kubefacets.com",
                    },
                    "policy": "POLICY_TYPE=Resource,POLICY_NAME=User",
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
                        "User - Delete",
                        summary="User Identifier",
                        value="USR=bc389855ad",
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
                        "User - Patch",
                        summary="User Identifier",
                        description="User - Patch",
                        value="USR=bc389855ad",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "User - Patch",
                value={
                    "attrs": {
                        "identifier": "USR=bc389855ad",
                        "first_name": "Gokul Nathan",
                        "middle_name": "",
                        "last_name": "Chandran",
                        "username": "gokul",
                        "type": "User",
                        "is_staff": False,
                        "is_superuser": False,
                        "is_active": True,
                        "is_email_verified": True,
                        "email": "gokul@kubefacets.com",
                    }
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "User - Patch",
                value={
                    "identifier": "USR=bc389855ad",
                    "type": "User",
                    "relations": [],
                    "children": [],
                    "parents": [],
                    "parent": None,
                    "created_by": None,
                    "is_public": False,
                    "attrs": {
                        "identifier": "USR=bc389855ad",
                        "first_name": "Gokul Nathan",
                        "middle_name": "",
                        "last_name": "Chandran",
                        "username": "gokul",
                        "type": "User",
                        "is_staff": False,
                        "is_superuser": False,
                        "is_active": True,
                        "is_email_verified": True,
                        "email": "gokul@kubefacets.com",
                    },
                    "policy": "POLICY_TYPE=Resource,POLICY_NAME=User",
                },
                request_only=False,
                response_only=True,
            ),
        ]
