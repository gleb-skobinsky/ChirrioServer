from django.http.request import HttpRequest
from django.http.response import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from chat.models import (ChirrioUser, ChatRoom, ChatRoomParticipant, Message)
from chat.serializers import UserRequestSerializer, UserResponseSerializer, MessageSerializer, MessageResponseSerializer


def index(request: HttpRequest) -> JsonResponse:
    return JsonResponse(data={"message": "Hello world"})


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh), str(refresh.access_token)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ChirrioUser.objects.all()
    serializer_class = UserResponseSerializer

    @swagger_auto_schema(
        request_body=UserRequestSerializer,
        responses={200: UserResponseSerializer()}
    )
    def retrieve(self, request):
        serializer = UserRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = ChirrioUser.objects.get(email=email)
        response_serializer = UserResponseSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class MessagesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "room_id",
                openapi.IN_PATH,
                description="Room id for messages",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: MessageResponseSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        room_id = self.kwargs["room_id"]
        db_room = ChatRoom.objects.get(chatroom_uid=room_id)
        messages = Message.objects.select_related().filter(chatroom_id=db_room)
        response_serializer = MessageResponseSerializer(messages, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):

    def post(self, request):
        try:
            email = request.data["email"]
            first_name = request.data["first_name"]
            last_name = request.data["last_name"]
            password = request.data["password"]
            user = ChirrioUser.objects.create_user(email=email, first_name=first_name, last_name=last_name,
                                                   password=password)
            access_token, refresh_token = get_tokens_for_user(user)
            return JsonResponse(
                data=user.toJSON(
                    access_token=access_token,
                    refresh_token=refresh_token
                )
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
            chat_rooms = [participant.chatroom_id.pk for participant in participants]
            rooms = [room.toJSON() for room in ChatRoom.objects.filter(pk__in=chat_rooms)]
            return JsonResponse(
                data={
                    "rooms": rooms
                }
            )
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SearchUsers(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            users = [user.toJSON() for user in ChirrioUser.objects.filter(email__icontains=request.data["email"])]
            print(users)
            return JsonResponse({
                "users": users
            })
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
