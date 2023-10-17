from datetime import datetime

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from chat.models import ChirrioUser, Message


class UserRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SignupSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class UserResponseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class UserAfterSignupSerializer(UserResponseSerializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChirrioUser
        fields = "__all__"


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MessageResponseSerializer(serializers.Serializer):
    chatroom_id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    text = serializers.CharField()
    created_at = serializers.DateTimeField()

    @swagger_serializer_method(serializer_or_field=UserResponseSerializer)
    def get_user_id(self, obj):
        return UserResponseSerializer(obj.user_id).data

    def get_chatroom_id(self, obj):
        return obj.chatroom_id.chatroom_uid

    def get_created_at(self, obj):
        created_at = obj.created_at
        formatted_date = datetime.strftime(created_at, '%Y-%m-%dT%H:%M:%S.%fZ')
        return formatted_date


class StringListField(serializers.ListField):
    child = serializers.CharField()


class ChatRoomResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    users = StringListField()


class ChatRoomsForUserSerializer(serializers.Serializer):
    chatroom_uid = serializers.CharField()
    chatroom_name = serializers.CharField()
    last_message = serializers.CharField()
    last_sent_user_id = serializers.SerializerMethodField()
    number_of_participants = serializers.IntegerField()

    @swagger_serializer_method(serializer_or_field=UserResponseSerializer)
    def get_last_sent_user_id(self, obj):
        return UserResponseSerializer(obj.last_sent_user_id).data
