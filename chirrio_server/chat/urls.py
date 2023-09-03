from django.urls import path, include

from . import views
from .routing import websocket_urlpatterns

urlpatterns = [
    path("", views.index),
]
