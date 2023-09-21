from django.http.request import HttpRequest
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from chat.models import ChirrioUser, ChatRoom, ChatRoomParticipant


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
            room_id = request.data["id"]
            name = request.data["name"]
            participants = request.data["users"]
            new_room = ChatRoom.objects.create(chatroom_uid=room_id, chatroom_name=name,
                                               number_of_participants=len(participants))
            new_room.save()
            chatroom_users = ChirrioUser.objects.filter(email__in=participants)
            for user in chatroom_users:
                db_participant = ChatRoomParticipant.objects.create(
                    user_id=user,
                    chatroom_id=new_room
                )
                db_participant.save()
            return JsonResponse(
                data=request.data
            )
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RequestRoomsByUser(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            user = ChirrioUser.objects.get_by_natural_key(request.data["email"])
            participants = ChatRoomParticipant.objects.filter(user_id=user)
            print(participants)
            chat_rooms = [participant.chatroom_id.pk for participant in participants]
            rooms = [room.toJSON() for room in ChatRoom.objects.filter(pk__in=chat_rooms)]
            return JsonResponse(
                data={
                    "rooms": rooms
                }
            )
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
