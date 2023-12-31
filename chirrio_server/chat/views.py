from django.http.request import HttpRequest
from django.http.response import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from chat.models import (ChirrioUser, ChatRoom, ChatRoomParticipant, Message)
from chat.serializers import UserResponseSerializer, MessageSerializer, MessageResponseSerializer, \
    ChatRoomResponseSerializer, ChatRoomsForUserSerializer, LogoutSerializer, SignupSerializer, \
    UserAfterSignupSerializer


def index(_: HttpRequest) -> JsonResponse:
    return JsonResponse(data={"message": "Hello world"})


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh), str(refresh.access_token)


class UserViewSet(viewsets.ModelViewSet):
    queryset = ChirrioUser.objects.all()
    serializer_class = UserResponseSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated, ]

        return super(UserViewSet, self).get_permissions()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "email",
                openapi.IN_PATH,
                description="Email to search for users",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: UserResponseSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        email = self.kwargs["email"]
        user = ChirrioUser.objects.get(email=email)
        response_serializer = UserResponseSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LogoutSerializer,
        responses={205: ""}
    )
    def destroy(self, request, *args, **kwargs):
        refresh_token = LogoutSerializer(request.data).data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)

    @swagger_auto_schema(
        request_body=SignupSerializer,
        responses={200: UserAfterSignupSerializer()}
    )
    def create(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.data
        user = ChirrioUser.objects.create_user(
            email=post["email"],
            first_name=post["first_name"],
            last_name=post["last_name"],
            password=post["password"],
            image=request.FILES.get('image')
        )
        refresh_token, access_token = get_tokens_for_user(user)
        response_serializer = UserAfterSignupSerializer(
            {"email": user.email,
             "first_name": user.first_name,
             "last_name": user.last_name,
             "image": user.image,
             "access_token": access_token,
             "refresh_token": refresh_token}
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "email",
                openapi.IN_PATH,
                description="Rooms for user",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: UserResponseSerializer(many=True)}
    )
    @action(detail=False, methods=['GET'])
    def search(self, request, *args, **kwargs):
        email = self.kwargs["email"]
        users = ChirrioUser.objects.filter(email__icontains=email)
        return Response(UserResponseSerializer(users, many=True).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "email",
                openapi.IN_PATH,
                description="List all users",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: UserResponseSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        users = ChirrioUser.objects.all()[:100]
        return Response(UserResponseSerializer(users, many=True).data, status=status.HTTP_200_OK)


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
        messages = Message.objects.select_related().filter(chatroom_id=db_room).order_by('-created_at')
        response_serializer = MessageResponseSerializer(messages, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class ChatRoomViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomResponseSerializer

    def create(self, request, *args, **kwargs):
        serializer = ChatRoomResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        users = serializer.data["users"]
        new_room = ChatRoom.objects.create(
            chatroom_uid=serializer.data["id"],
            chatroom_name=serializer.data["name"],
            number_of_participants=len(users)
        )
        new_room.save()
        chatroom_users = ChirrioUser.objects.filter(email__in=users)
        for user in chatroom_users:
            db_participant = ChatRoomParticipant.objects.create(
                user_id=user,
                chatroom_id=new_room
            )
            db_participant.save()
        return Response(ChatRoomResponseSerializer(request.data).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "email",
                openapi.IN_PATH,
                description="Rooms for user",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: ChatRoomsForUserSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        email = self.kwargs["email"]
        user = ChirrioUser.objects.get_by_natural_key(email)
        participants = ChatRoomParticipant.objects.filter(user_id=user)
        chat_room_ids = [participant.chatroom_id.pk for participant in participants]
        chat_rooms = ChatRoom.objects.filter(pk__in=chat_room_ids)
        return Response(ChatRoomsForUserSerializer(chat_rooms, many=True).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "room_id",
                openapi.IN_PATH,
                description="Id of the room to get",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: ChatRoomsForUserSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        chat = ChatRoom.objects.get(chatroom_uid=self.kwargs["room_id"])
        response_serializer = ChatRoomsForUserSerializer(chat)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
