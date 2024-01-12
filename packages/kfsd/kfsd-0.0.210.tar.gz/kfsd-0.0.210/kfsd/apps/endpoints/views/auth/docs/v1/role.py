from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class RoleDocV1:
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
                "Role - List All",
                value=[
                    {
                        "identifier": "RLE=632032fb35",
                        "type": "Role",
                        "relations": [],
                        "children": [],
                        "parents": [],
                        "parent": None,
                        "created_by": None,
                        "is_public": False,
                        "attrs": {
                            "identifier": "RLE=632032fb35",
                            "name": "Staff",
                            "slug": "staff",
                            "created_by": "RLE=632032fb35",
                            "desc": "Kubefacets Staff",
                        },
                        "policy": "POLICY_TYPE=Resource,POLICY_NAME=Role",
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
                        "Role - Get",
                        summary="Role Identifier",
                        description="Role - Get",
                        value="RLE=632032fb35",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Role - Get",
                value={
                    "identifier": "RLE=632032fb35",
                    "type": "Role",
                    "relations": [],
                    "children": [],
                    "parents": [],
                    "parent": None,
                    "created_by": None,
                    "is_public": False,
                    "attrs": {
                        "identifier": "RLE=632032fb35",
                        "name": "Staff",
                        "slug": "staff",
                        "created_by": "RLE=632032fb35",
                        "desc": "Kubefacets Staff",
                    },
                    "policy": "POLICY_TYPE=Resource,POLICY_NAME=Role",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Role - Create",
                value={
                    "identifier": "RLE=632032fb35",
                    "created_by": None,
                    "is_public": False,
                    "attrs": {
                        "identifier": "RLE=632032fb35",
                        "name": "Staff",
                        "slug": "staff",
                        "created_by": "RLE=632032fb35",
                        "desc": "Kubefacets Staff",
                    },
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Role - Create",
                value={
                    "identifier": "RLE=632032fb35",
                    "type": "Role",
                    "relations": [],
                    "children": [],
                    "parents": [],
                    "parent": None,
                    "created_by": None,
                    "is_public": False,
                    "attrs": {
                        "identifier": "RLE=632032fb35",
                        "name": "Staff",
                        "slug": "staff",
                        "created_by": "RLE=632032fb35",
                        "desc": "Kubefacets Staff",
                    },
                    "policy": "POLICY_TYPE=Resource,POLICY_NAME=Role",
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
                        "Role - Delete",
                        summary="Role Identifier",
                        value="RLE=632032fb35",
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
                        "Role - Patch",
                        summary="Role Identifier",
                        description="Role - Patch",
                        value="RLE=632032fb35",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Role - Patch",
                value={
                    "attrs": {
                        "identifier": "RLE=632032fb35",
                        "name": "Staff",
                        "slug": "staff",
                        "created_by": "RLE=632032fb35",
                        "desc": "Kubefacets Staff",
                    }
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Role - Patch",
                value={
                    "identifier": "RLE=632032fb35",
                    "type": "Role",
                    "relations": [],
                    "children": [],
                    "parents": [],
                    "parent": None,
                    "created_by": None,
                    "is_public": False,
                    "attrs": {
                        "identifier": "RLE=632032fb35",
                        "name": "Staff",
                        "slug": "staff",
                        "created_by": "RLE=632032fb35",
                        "desc": "Kubefacets Staff",
                    },
                    "policy": "POLICY_TYPE=Resource,POLICY_NAME=Role",
                },
                request_only=False,
                response_only=True,
            ),
        ]
