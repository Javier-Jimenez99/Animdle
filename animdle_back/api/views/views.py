import secrets

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

from ..models import Anime, Result
from ..serializers import AnimdleUserSerializer, AnimeSerializer
from .utils import (
    get_all_synonyms_relations,
    get_all_titles,
    get_day_by_date,
    get_theme,
    japan_date,
)


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
                "guest": True,
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
        try:
            day_obj = get_day_by_date(japan_date())
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
        try:
            day_obj = get_day_by_date(japan_date())
            theme_data = get_theme(game_mode, day_obj)

            return Response(
                {"video_url": theme_data["video_url"]}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def game_state(request, game_mode, date=japan_date()):
    if request.method == "GET":
        # Restore after tryings
        if date > japan_date():
            return Response(
                {"error": "You can't play in the future"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_obj = request.user

        day_obj = get_day_by_date(date)

        result_obj, created = Result.objects.get_or_create(
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


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def guess(request, game_mode, date=japan_date()):
    if request.method == "POST":
        # Restore after tryings
        if date > japan_date():
            return Response(
                {"error": "You can't play in the future"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_obj = request.user

        day_obj = get_day_by_date(date)

        try:
            result_obj = Result.objects.get(
                user=user_obj, day=day_obj, game_mode=game_mode
            )
        except Result.DoesNotExist:
            return Response(
                {"error": "You must start the game first"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if result_obj.state != "pending":
            return Response(
                {"error": "You already finished the game"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        theme_obj = getattr(day_obj, game_mode)
        anime_obj = theme_obj.anime

        all_animes_relations = get_all_synonyms_relations()

        # Allways save the title attempt
        attempts = eval(result_obj.attempts)
        title = request.data["title"]
        attempts.append(title)
        result_obj.attempts = str(attempts)

        # Check if the title is correct
        if (
            title in all_animes_relations.keys()
            and all_animes_relations[title] == anime_obj.title
        ):
            result_obj.state = "win"

        # If not, check if the user has more attempts
        # Else result_obj.state = "pending"
        elif len(attempts) >= 5:
            result_obj.state = "lose"

        result_obj.save()

        response_data = {
            "attempts": eval(result_obj.attempts),
            "state": result_obj.state,
        }
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def results(request, game_mode, date=japan_date()):
    if request.method == "GET":
        user_obj = request.user

        day_obj = get_day_by_date(date)

        try:
            result_obj = Result.objects.get(
                user=user_obj, day=day_obj, game_mode=game_mode
            )
        except Result.DoesNotExist:
            return Response(
                {"error": "You must start the game first"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if result_obj.state == "pending":
            return Response(
                {"error": "You must finish the game first"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        theme = getattr(day_obj, game_mode)
        anime = theme.anime

        response_data = {
            "title": anime.title,
            "image_url": anime.image_url,
            "video_url": theme.video_url,
            "song": theme.title,
            "state": result_obj.state,
            "attempts": eval(result_obj.attempts),
            "synopsis": anime.synopsis.replace("\n", "").replace("<br>", "</br>"),
        }

        return Response(response_data, status=status.HTTP_200_OK)
