from django.http.request import HttpRequest
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from chat.models import ChirrioUser


def index(request: HttpRequest) -> JsonResponse:
    return JsonResponse(data={"message": "Hello world"})


class GetUser(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            email = request.data["email"]
            access = request.data["accessToken"]
            refresh = request.data["refreshToken"]
            user = ChirrioUser.objects.get(email=email)
            return JsonResponse(
                data={
                    "email": user.email,
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                    "accessToken": access,
                    "refreshToken": refresh
                }
            )
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refreshToken"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
