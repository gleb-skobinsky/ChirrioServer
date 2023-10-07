from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from chat.views import (index, LogoutView, SignupView, CreateChatRoom, RequestRoomsByUser,
                        SearchUsers, UserViewSet, MessagesViewSet)

urlpatterns = [
    path("", index),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignupView.as_view(), name="sign up"),
    path("login/",
         jwt_views.TokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("token/refresh/",
         jwt_views.TokenRefreshView.as_view(),
         name="token_refresh"),
    path("new-room/", CreateChatRoom.as_view(), name="create new room"),
    path("rooms-by-user/", RequestRoomsByUser.as_view(), name="request rooms by user"),
    path("user-search/", SearchUsers.as_view(), name="search users"),

    path("user/", UserViewSet.as_view({'post': 'retrieve'}), name="get user"),
    path(
        "messages-by-room/<str:room_id>/",
        MessagesViewSet.as_view({"get": "list"}),
        name="request messages by room"
    ),
]
