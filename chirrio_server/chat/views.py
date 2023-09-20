from django.http.request import HttpRequest
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from chat.models import ChirrioUser, ChatRoom


def index(request: HttpRequest) -> JsonResponse:
    return JsonResponse(data={"message": "Hello world"})


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh), str(refresh.access_token)


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


class SignupView(APIView):

    def post(self, request):
        try:
            email = request.data["email"]
            first_name = request.data["firstName"]
            last_name = request.data["lastName"]
            password = request.data["password"]
            user = ChirrioUser.objects.create_user(email=email, first_name=first_name, last_name=last_name,
                                                   password=password)
            access_token, refresh_token = get_tokens_for_user(user)
            return JsonResponse(
                data={
                    "email": user.email,
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                    "accessToken": access_token,
                    "refreshToken": refresh_token
                }
            )
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateChatRoom(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            print(request.data)
            room_id = request.data["id"]
            name = request.data["name"]
            participants = request.data["users"]
            new_room = ChatRoom.objects.create(chatroom_uid=room_id, chatroom_name=name,
                                               number_of_participants=len(participants))
            new_room.save()
            return JsonResponse(
                data=request.data
            )
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
