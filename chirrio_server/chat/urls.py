from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from chat.views import (index, UserViewSet, MessagesViewSet, ChatRoomViewSet)

urlpatterns = [
    path("", index),
    path(
        "messages/<str:room_id>/",
        MessagesViewSet.as_view({"get": "list"}),
        name="request messages by room"
    ),

    path("rooms/create/", ChatRoomViewSet.as_view({"post": "create"}), name="create new room"),
    path("rooms/<str:email>/", ChatRoomViewSet.as_view({"get": "list"}), name="request rooms by user"),
    path("rooms/get/<str:room_id>/", ChatRoomViewSet.as_view({"get": "retrieve"}), name="request room by id"),

    path("users/logout/", UserViewSet.as_view({"post": "destroy"}), name="logout"),
    path("users/signup/", UserViewSet.as_view({"post": "create"}), name="sign up"),
    path("users/login/",
         jwt_views.TokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("users/refresh-token/",
         jwt_views.TokenRefreshView.as_view(),
         name="token_refresh"),
    path("users/search/<str:email>/", UserViewSet.as_view({"get": "list"}), name="search users"),
    path("users/<str:email>/", UserViewSet.as_view({'get': 'retrieve'}), name="get user"),
]
