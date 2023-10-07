from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from chat.models import ChirrioUser, Message


class UserRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserResponseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChirrioUser
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MessageResponseSerializer(serializers.Serializer):
    chatroom_id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    text = serializers.CharField()
    created_at = serializers.CharField()

    @swagger_serializer_method(serializer_or_field=UserResponseSerializer)
    def get_user_id(self, obj):
        return UserResponseSerializer(obj.user_id).data

    def get_chatroom_id(self, obj):
        return obj.chatroom_id.chatroom_uid
