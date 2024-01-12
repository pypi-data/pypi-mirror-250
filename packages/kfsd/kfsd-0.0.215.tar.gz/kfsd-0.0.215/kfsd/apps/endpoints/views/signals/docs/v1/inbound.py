from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class InboundV1Doc:
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
                "Inbound - List All",
                value=[
                    {
                        "identifier": "a24fda59a44fce8f376435221d9514a2",
                        "data": {
                            "meta": {
                                "op": "CREATE",
                                "service_id": "sso_api",
                                "tbl": "user",
                            },
                            "user": {
                                "identifier": "USER=admin@kubefacets.com",
                                "email": "admin@kubefacets.com",
                                "username": "admin",
                                "is_staff": True,
                                "is_active": True,
                                "is_superuser": True,
                                "is_email_verified": True,
                                "first_name": "Gokul Nathan",
                                "last_name": "Chandran",
                                "slug": "admin",
                                "created": "2022-07-03T05:40:08.286504Z",
                                "updated": "2022-07-03T05:40:08.286504Z",
                            },
                        },
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
                        "Inbound - Get",
                        summary="Inbound Identifier",
                        description="Inbound - Get",
                        value="a24fda59a44fce8f376435221d9514a2",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Inbound - Get",
                value={
                    "identifier": "a24fda59a44fce8f376435221d9514a2",
                    "data": {
                        "meta": {
                            "op": "CREATE",
                            "service_id": "sso_api",
                            "tbl": "User",
                        },
                        "data": {
                            "identifier": "USER=admin@kubefacets.com",
                            "email": "admin@kubefacets.com",
                            "username": "admin",
                            "is_staff": True,
                            "is_active": True,
                            "is_superuser": True,
                            "is_email_verified": True,
                            "first_name": "Gokul Nathan",
                            "last_name": "Chandran",
                            "slug": "admin",
                            "created": "2022-07-03T05:40:08.286504Z",
                            "updated": "2022-07-03T05:40:08.286504Z",
                        },
                    },
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Inbound - Create (CLEAR_INBOUND)",
                value={
                    "name": "CLEAR_INBOUND",
                    "data": {"action": "CLEAR_INBOUND", "data": {}},
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Inbound - Create (CLEAR_OUTBOUND)",
                value={
                    "name": "CLEAR_OUTBOUND",
                    "data": {"action": "CLEAR_OUTBOUND", "data": {}},
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Inbound - Create",
                value={
                    "identifier": "abcde",
                    "name": "CLEAR_OUTBOUND",
                    "data": {},
                    "status": "IN-PROGRESS",
                    "attempts": 0,
                    "debug_info": {},
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
                        "Inbound - Delete",
                        summary="Inbound Identifier",
                        description="Inbound - Delete",
                        value="abcde",
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
                        "Inbound - Patch",
                        summary="Inbound Identifier",
                        description="Inbound - Patch",
                        value="abcde",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Inbound - Patch",
                value={
                    "name": "CLEAR_OUTBOUND",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Inbound - Patch",
                value={
                    "identifier": "abcde",
                    "name": "CLEAR_OUTBOUND",
                    "data": {"name": "123"},
                    "status": "IN-PROGRESS",
                    "attempts": 0,
                    "debug_info": {},
                },
                request_only=False,
                response_only=True,
            ),
        ]
