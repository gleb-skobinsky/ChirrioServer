from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from chat.views import (index, LogoutView, GetUser, SignupView, CreateChatRoom, RequestRoomsByUser,
                        RequestMessagesByRoom)

urlpatterns = [
    path("", index),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/", GetUser.as_view(), name="get user"),
    path("signup/", SignupView.as_view(), name="sign up"),
    path("token/",
         jwt_views.TokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("token/refresh/",
         jwt_views.TokenRefreshView.as_view(),
         name="token_refresh"),
    path("new-room/", CreateChatRoom.as_view(), name="create new room"),
    path("rooms-by-user/", RequestRoomsByUser.as_view(), name="request rooms by user"),
    path("messages-by-room/", RequestMessagesByRoom.as_view(), name="request messages by room")
]
