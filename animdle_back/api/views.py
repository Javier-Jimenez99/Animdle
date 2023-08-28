from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import AnimdleUser, Anime, Day, Result, Theme


@api_view(["POST"])
def create_anime(request):
    if request.method == "POST":
        data = request.data
        anime = Anime.objects.create(**data)
        return Response(
            {"message": "Anime created successfully"}, status=status.HTTP_201_CREATED
        )


@api_view(["POST"])
def create_theme(request):
    if request.method == "POST":
        data = request.data
        theme = Theme.objects.create(**data)
        return Response(
            {"message": "Theme created successfully"}, status=status.HTTP_201_CREATED
        )


@api_view(["POST"])
def create_day(request):
    if request.method == "POST":
        data = request.data
        day = Day.objects.create(**data)
        return Response(
            {"message": "Day created successfully"}, status=status.HTTP_201_CREATED
        )


@api_view(["POST"])
def create_result(request):
    if request.method == "POST":
        data = request.data
        result = Result.objects.create(**data)
        return Response(
            {"message": "Result created successfully"}, status=status.HTTP_201_CREATED
        )


@api_view(["POST"])
def create_user(request):
    if request.method == "POST":
        data = request.data
        user = AnimdleUser.objects.create(**data)
        return Response(
            {"message": "User created successfully"}, status=status.HTTP_201_CREATED
        )
