import secrets
from datetime import datetime as dt

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Anime, Day, Result, Theme
from ..serializers import (
    AnimdleUserSerializer,
    AnimeSerializer,
    DaySerializer,
    ThemeSerializer,
)
from .utils import check_game_mode, get_all_titles, get_theme, get_today_day


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
def create_guest(request):
    if request.method == "POST":
        browser_id = secrets.token_hex(16)
        username = "guest-" + browser_id

        serializer = AnimdleUserSerializer(
            data={
                "username": username,
                "user_browser_id": browser_id,
                "password": "guest",
            }
        )
        if serializer.is_valid():
            user_obj = serializer.save()
            user_obj.set_password("guest")
            user_obj.save()
            token_obj = Token.objects.create(user=user_obj)

            response_data = {"token": str(token_obj), "browser_id": browser_id}

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def todays_anime(request, game_mode):
    if request.method == "GET":
        game_mode = check_game_mode(game_mode)

        if isinstance(game_mode, Response):
            return game_mode

        try:
            day_obj = get_today_day()
            theme_data = get_theme(game_mode, day_obj)
            id_anime = theme_data["anime"]

            anime_obj = Anime.objects.get(id=id_anime)
            serializer = AnimeSerializer(anime_obj)
            anime_obj = serializer.data

            response_data = theme_data
            response_data["anime"] = anime_obj

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def todays_video(request, game_mode):
    if request.method == "GET":
        game_mode = check_game_mode(game_mode)

        if isinstance(game_mode, Response):
            return game_mode

        try:
            day_obj = get_today_day()
            theme_data = get_theme(game_mode, day_obj)

            return Response(
                {"video_url": theme_data["video_url"]}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def game_state(request, game_mode, date="today"):
    if request.method == "GET":
        game_mode = check_game_mode(game_mode)

        if isinstance(game_mode, Response):
            return game_mode

        user_obj = request.user

        if date == "today":
            day_obj = get_today_day()
        else:
            date = dt.strptime(date, "%Y-%m-%d")
            day_obj = Day.objects.get(date=date)

        try:
            result_obj = Result.objects.get(
                user=user_obj, day=day_obj, game_mode=game_mode
            )
        except Result.DoesNotExist:
            result_obj = Result.objects.create(
                user=user_obj, day=day_obj, game_mode=game_mode
            )

        theme_data = get_theme(game_mode, day_obj)
        all_titles = get_all_titles()

        response_data = {
            "state": result_obj.state,
            "attempts": eval(result_obj.attempts),
            "video_url": theme_data["video_url"],
            "all_titles": all_titles,
        }

        return Response(response_data, status=status.HTTP_200_OK)
