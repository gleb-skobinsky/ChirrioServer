from rest_framework import serializers

from chat.models import ChirrioUser


class UserRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserResponseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChirrioUser
        fields = '__all__'
