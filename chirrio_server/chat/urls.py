from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from chat.views import (index, LogoutView, GetUser, SignupView)

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
         name="token_refresh")
]
