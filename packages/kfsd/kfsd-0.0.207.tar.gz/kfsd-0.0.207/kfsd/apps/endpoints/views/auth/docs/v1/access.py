from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class AccessDocV1:
    @staticmethod
    def modelviewset_partial_update_examples():
        return [
            OpenApiExample(
                "Access - Partial Update",
                value={"permission": ["can_view", "can_edit", "can_delete"]},
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Access - Partial Update",
                value={
                    "identifier": "ACTOR=USR=76598a194e,RESOURCE=ORG=7d0c12635d",
                    "actor": "USR=76598a194e",
                    "resource": "ORG=7d0c12635d",
                    "permissions": "['can_view', 'can_edit', 'can_delete']",
                },
                request_only=False,
                response_only=True,
            ),
        ]

    @staticmethod
    def modelviewset_partial_update_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Access - Partial Update",
                        summary="Access Identifier",
                        description="Access - Partial Update",
                        value="ACTOR=USR=76598a194e,RESOURCE=ORG=7d0c12635d",
                    )
                ],
            )
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
                        "Example 1",
                        summary="Access Identifier",
                        value="ACTOR=USR=76598a194e,RESOURCE=ORG=7d0c12635d",
                    )
                ],
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
                        "Example 1",
                        summary="Access Identifier",
                        value="ACTOR=USR=76598a194e,RESOURCE=ORG=7d0c12635d",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Access - Get",
                value={
                    "identifier": "ACTOR=USR=76598a194e,RESOURCE=ORG=7d0c12635d",
                    "actor": "USR=76598a194e",
                    "resource": "ORG=7d0c12635d",
                    "permissions": "['can_view', 'can_edit', 'can_delete']",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Access - Create",
                value={
                    "actor": "USR=76598a194e",
                    "resource": "ORG=7d0c12635d",
                    "permissions": "['can_view', 'can_edit', 'can_delete']",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Access - Create",
                value={
                    "identifier": "ACTOR=USR=76598a194e,RESOURCE=ORG=7d0c12635d",
                    "actor": "USR=76598a194e",
                    "resource": "ORG=7d0c12635d",
                    "permissions": "['can_view', 'can_edit', 'can_delete']",
                },
                request_only=False,
                response_only=True,
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
                "Access - Get All",
                value=[
                    {
                        "identifier": "ACTOR=USR=76598a194e,RESOURCE=ORG=7d0c12635d",
                        "actor": "USR=76598a194e",
                        "resource": "ORG=7d0c12635d",
                        "permissions": "['can_view', 'can_edit', 'can_delete']",
                    },
                ],
            )
        ]
