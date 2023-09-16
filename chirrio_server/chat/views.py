from django.contrib.auth import authenticate, login
from django.http.request import HttpRequest
from django.http.response import JsonResponse


def index(request: HttpRequest) -> JsonResponse:
    return JsonResponse(data={"message": "Hello world"})


def login_user(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse(data={"message": "Login successful"})
        else:
            return JsonResponse(status=403, data={"message": "Login unsuccessful"})
    else:
        return JsonResponse(status=403, data={"Error": "Unsupported method"})
