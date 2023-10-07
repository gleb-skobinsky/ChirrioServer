from rest_framework.schemas import AutoSchema, coreapi


class GetUserSchema(AutoSchema):
    manual_fields = []  # common fields

    def get_manual_fields(self, path, method):
        custom_fields = []
        if method.lower() == "get":
            custom_fields = [
                coreapi.Field(
                    "email",
                    required=True,
                    location='query',
                    description="User's email"
                ),
                coreapi.Field(
                    "access_token",
                    required=True,
                    location='query',
                    description="User's access token"
                ),
                coreapi.Field(
                    "refresh_token",
                    required=True,
                    location='query',
                    description="User's refresh token"
                ),
            ]
        if method.lower() == "post":
            custom_fields = [
                coreapi.Field(
                    "email",
                    required=True,
                    location='query',
                    description="User's email"
                ),
                coreapi.Field(
                    "access_token",
                    required=True,
                    location='query',
                    description="User's access token"
                ),
                coreapi.Field(
                    "refresh_token",
                    required=True,
                    location='query',
                    description="User's refresh token"
                ),
            ]
        return self._manual_fields + custom_fields
