from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class TeamDocV1:
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
                "Team - List All",
                value=[
                    {
                        "identifier": "TEM=73fe3df7d0",
                        "type": "Team",
                        "relations": [],
                        "children": [],
                        "parents": [],
                        "parent": None,
                        "created_by": None,
                        "is_public": False,
                        "attrs": {
                            "identifier": "TEM=73fe3df7d0",
                            "name": "Config FE",
                            "slug": "config-fe",
                            "created_by": "TEM=73fe3df7d0",
                            "desc": "Kubefacets FE Team",
                        },
                        "policy": "POLICY_TYPE=Resource,POLICY_NAME=Team",
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
                        "Team - Get",
                        summary="Team Identifier",
                        description="Team - Get",
                        value="TEM=73fe3df7d0",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Team - Get",
                value={
                    "identifier": "TEM=73fe3df7d0",
                    "type": "Team",
                    "relations": [],
                    "children": [],
                    "parents": [],
                    "parent": None,
                    "created_by": None,
                    "is_public": False,
                    "attrs": {
                        "identifier": "TEM=73fe3df7d0",
                        "name": "Config FE",
                        "slug": "config-fe",
                        "created_by": "TEM=73fe3df7d0",
                        "desc": "Kubefacets FE Team",
                    },
                    "policy": "POLICY_TYPE=Resource,POLICY_NAME=Team",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Team - Create",
                value={
                    "identifier": "TEM=73fe3df7d0",
                    "type": "Team",
                    "created_by": None,
                    "is_public": False,
                    "attrs": {
                        "identifier": "TEM=73fe3df7d0",
                        "name": "Config FE",
                        "slug": "config-fe",
                        "created_by": "TEM=73fe3df7d0",
                        "desc": "Kubefacets FE Team",
                    },
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Team - Create",
                value={
                    "identifier": "TEM=73fe3df7d0",
                    "type": "Team",
                    "relations": [],
                    "children": [],
                    "parents": [],
                    "parent": None,
                    "created_by": None,
                    "is_public": False,
                    "attrs": {
                        "identifier": "TEM=73fe3df7d0",
                        "name": "Config FE",
                        "slug": "config-fe",
                        "created_by": "TEM=73fe3df7d0",
                        "desc": "Kubefacets FE Team",
                    },
                    "policy": "POLICY_TYPE=Resource,POLICY_NAME=Team",
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
                        "Team - Delete",
                        summary="Team Identifier",
                        value="TEM=73fe3df7d0",
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
                        "Team - Patch",
                        summary="Team Identifier",
                        description="Team - Patch",
                        value="TEM=73fe3df7d0",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Team - Patch",
                value={
                    "attrs": {
                        "identifier": "TEM=73fe3df7d0",
                        "name": "Config FE",
                        "slug": "config-fe",
                        "created_by": "TEM=73fe3df7d0",
                        "desc": "Kubefacets FE Team",
                    }
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Team - Patch",
                value={
                    "identifier": "TEM=73fe3df7d0",
                    "type": "Team",
                    "relations": [],
                    "children": [],
                    "parents": [],
                    "parent": None,
                    "created_by": None,
                    "is_public": False,
                    "attrs": {
                        "identifier": "TEM=73fe3df7d0",
                        "name": "Config FE",
                        "slug": "config-fe",
                        "created_by": "TEM=73fe3df7d0",
                        "desc": "Kubefacets FE Team",
                    },
                    "policy": "POLICY_TYPE=Resource,POLICY_NAME=Team",
                },
                request_only=False,
                response_only=True,
            ),
        ]
