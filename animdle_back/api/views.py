from datetime import datetime as dt

import pytz
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import AnimdleUser, Anime, Day, Result, Theme
from .serializers import (
    AnimdleUserSerializer,
    AnimeSerializer,
    DaySerializer,
    ResultSerializer,
    ThemeSerializer,
)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_anime(request):
    if request.method == "POST":
        try:
            anime = Anime.objects.get(id=request.data["id"])
            serializer = AnimeSerializer(anime, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Anime.DoesNotExist:
            serializer = AnimeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_theme(request):
    if request.method == "POST":
        try:
            theme = Theme.objects.get(id=request.data["id"])
            serializer = ThemeSerializer(theme, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Theme.DoesNotExist:
            serializer = ThemeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_day(request):
    if request.method == "POST":
        try:
            day = Day.objects.get(id=request.data["id"])
            serializer = DaySerializer(day, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Day.DoesNotExist:
            serializer = DaySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_result(request):
    if request.method == "POST":
        try:
            result = Result.objects.get(id=request.data["id"])
            serializer = ResultSerializer(result, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Result.DoesNotExist:
            serializer = ResultSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_user(request):
    if request.method == "POST":
        try:
            user = AnimdleUser.objects.get(id=request.data["id"])
            serializer = AnimdleUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AnimdleUser.DoesNotExist:
            serializer = AnimdleUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def todays_anime(request, game_mode):
    if request.method == "GET":
        if game_mode not in [
            "opening",
            "hardcore-opening",
            "ending",
            "hardcore-ending",
        ]:
            return Response(
                {"error": "Invalid game mode"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            japan_date = dt.now(tz=pytz.timezone("Asia/Tokyo"))
            year = japan_date.year
            month = japan_date.month
            day = japan_date.day

            day_obj = Day.objects.filter(
                date__year=year, date__month=month, date__day=day
            )

            if len(day_obj) == 0:
                return Response(
                    {"error": "No anime for today"}, status=status.HTTP_400_BAD_REQUEST
                )

            day_obj = day_obj[0]
            serializer = DaySerializer(day_obj)
            day_obj = serializer.data

            if game_mode == "opening":
                id_theme = day_obj["easy_opening"]
            elif game_mode == "hardcore-opening":
                id_theme = day_obj["hardcore_opening"]
            elif game_mode == "ending":
                id_theme = day_obj["easy_ending"]
            elif game_mode == "hardcore-ending":
                id_theme = day_obj["hardcore_ending"]

            theme_obj = Theme.objects.get(id=id_theme)
            serializer = ThemeSerializer(theme_obj)
            theme_obj = serializer.data
            id_anime = theme_obj["anime"]

            anime_obj = Anime.objects.get(id=id_anime)
            serializer = AnimeSerializer(anime_obj)
            anime_obj = serializer.data

            response_data = theme_obj
            response_data["anime"] = anime_obj

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
