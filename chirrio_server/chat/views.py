from django.http.request import HttpRequest
from django.http.response import JsonResponse


def index(request: HttpRequest) -> JsonResponse:
    return JsonResponse(data={"message": "Hello world"})
