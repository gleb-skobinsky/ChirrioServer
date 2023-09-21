from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as lazy


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def _create_user(self, email, password, is_staff, is_superuser, first_name, last_name, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(lazy("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(
            self, email, password=None, is_staff=False, is_superuser=False, first_name="", last_name="", **extra_fields
    ):
        return self._create_user(
            email=email,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(lazy("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(lazy("Superuser must have is_superuser=True."))
        return self.create_user(email, password, True, True)


class ChirrioUser(AbstractBaseUser, PermissionsMixin):
    useruid = models.CharField(max_length=36, default=str(uuid4()))
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=200, default="")
    email = models.EmailField(lazy("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def toJSON(self, access_token: str = "", refresh_token: str = "") -> dict:
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "access_token": access_token,
            "refresh_token": refresh_token
        }


class ChatRoom(models.Model):
    chatroom_uid = models.CharField(max_length=36, default=str(uuid4()))
    chatroom_name = models.CharField(max_length=1024, default="")
    last_message = models.CharField(max_length=2048, default="")
    last_sent_user_id = models.ForeignKey(ChirrioUser, on_delete=models.PROTECT, default=1)
    number_of_participants = models.IntegerField(default=1)

    def toJSON(self):
        return {
            "chatroom_uid": self.chatroom_uid,
            "chatroom_name": self.chatroom_name,
            "last_message": self.last_message,
            "last_sent_user_id": self.last_sent_user_id.toJSON(),
            "number_of_participants": self.number_of_participants
        }


class Message(models.Model):
    chatroom_id = models.ForeignKey(ChatRoom, on_delete=models.PROTECT, default=1)
    user_id = models.ForeignKey(ChirrioUser, on_delete=models.PROTECT, default=1)
    text = models.CharField(max_length=2048, default="")
    created_at = models.DateTimeField(auto_now=True)


class ChatRoomParticipant(models.Model):
    user_id = models.ForeignKey(ChirrioUser, on_delete=models.CASCADE, default=1)
    chatroom_id = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, default=1)
