from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class OrgDocV1:
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
                "Org - List All",
                value=[
                    {
                        "identifier": "ORG=7d0c12635d",
                        "type": "Org",
                        "relations": [],
                        "children": [
                            {"child": "PRJ=9b3936aa84", "child_type": "Project"}
                        ],
                        "parents": [],
                        "parent": None,
                        "created_by": None,
                        "is_public": False,
                        "attrs": {
                            "identifier": "ORG=7d0c12635d",
                            "name": "Kubefacets",
                            "slug": "kubefacets",
                            "created_by": "ORG=7d0c12635d",
                            "desc": "Kubefacets Organization",
                        },
                        "policy": "POLICY_TYPE=Resource,POLICY_NAME=Org",
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
                        "Org - Get",
                        summary="Org Identifier",
                        description="Org - Get",
                        value="ORG=7d0c12635d",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Org - Get",
                value={
                    "identifier": "ORG=7d0c12635d",
                    "type": "Org",
                    "relations": [],
                    "children": [{"child": "PRJ=9b3936aa84", "child_type": "Project"}],
                    "parents": [],
                    "parent": None,
                    "created_by": None,
                    "is_public": False,
                    "attrs": {
                        "identifier": "ORG=7d0c12635d",
                        "name": "Kubefacets",
                        "slug": "kubefacets",
                        "created_by": "ORG=7d0c12635d",
                        "desc": "Kubefacets Organization",
                    },
                    "policy": "POLICY_TYPE=Resource,POLICY_NAME=Org",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Org - Create",
                value={
                    "identifier": "ORG=7d0c12635d",
                    "is_public": False,
                    "attrs": {
                        "identifier": "ORG=7d0c12635d",
                        "name": "Kubefacets",
                        "slug": "kubefacets",
                        "created_by": "ORG=7d0c12635d",
                        "desc": "Kubefacets Organization",
                    },
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Org - Create",
                value={
                    "identifier": "ORG=7d0c12635d",
                    "type": "Org",
                    "relations": [],
                    "children": [{"child": "PRJ=9b3936aa84", "child_type": "Project"}],
                    "parents": [],
                    "parent": None,
                    "created_by": None,
                    "is_public": False,
                    "attrs": {
                        "identifier": "ORG=7d0c12635d",
                        "name": "Kubefacets",
                        "slug": "kubefacets",
                        "created_by": "ORG=7d0c12635d",
                        "desc": "Kubefacets Organization",
                    },
                    "policy": "POLICY_TYPE=Resource,POLICY_NAME=Org",
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
                        "Org - Delete",
                        summary="Org Identifier",
                        value="ORG=7d0c12635d",
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
                        "Org - Patch",
                        summary="Org Identifier",
                        description="Org - Patch",
                        value="ORG=7d0c12635d",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Org - Patch",
                value={
                    "attrs": {
                        "identifier": "ORG=7d0c12635d",
                        "name": "Kubefacets",
                        "slug": "kubefacets",
                        "created_by": "ORG=7d0c12635d",
                        "desc": "Kubefacets Organization",
                    }
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Org - Patch",
                value={
                    "identifier": "ORG=7d0c12635d",
                    "type": "Org",
                    "relations": [],
                    "children": [{"child": "PRJ=9b3936aa84", "child_type": "Project"}],
                    "parents": [],
                    "parent": None,
                    "created_by": None,
                    "is_public": False,
                    "attrs": {
                        "identifier": "ORG=7d0c12635d",
                        "name": "Kubefacets",
                        "slug": "kubefacets",
                        "created_by": "ORG=7d0c12635d",
                        "desc": "Kubefacets Organization",
                    },
                    "policy": "POLICY_TYPE=Resource,POLICY_NAME=Org",
                },
                request_only=False,
                response_only=True,
            ),
        ]
