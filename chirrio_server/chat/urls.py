from django.urls import path

from chat.views import login_user

urlpatterns = [
    path("api/login/", login_user),
]
