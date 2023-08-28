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
        serializer = AnimeSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data["title"]

            # Utiliza get_or_create para buscar o crear el anime
            anime, created = Anime.objects.get_or_create(
                title=title, defaults=serializer.validated_data
            )

            # Si el anime ya existía, actualiza los campos con los nuevos datos
            if not created:
                serializer.update(anime, serializer.validated_data)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_theme(request):
    if request.method == "POST":
        serializer = ThemeSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data["title"]

            # Utiliza get_or_create para buscar o crear el tema
            theme, created = Theme.objects.get_or_create(
                title=title, defaults=serializer.validated_data
            )

            # Si el tema ya existía, actualiza los campos con los nuevos datos
            if not created:
                serializer.update(theme, serializer.validated_data)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_day(request):
    if request.method == "POST":
        serializer = DaySerializer(data=request.data)
        if serializer.is_valid():
            date = serializer.validated_data["date"]

            # Utiliza get_or_create para buscar o crear el día
            day, created = Day.objects.get_or_create(
                date=date, defaults=serializer.validated_data
            )

            # Si el día ya existía, actualiza los campos con los nuevos datos
            if not created:
                serializer.update(day, serializer.validated_data)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_result(request):
    if request.method == "POST":
        serializer = ResultSerializer(data=request.data)
        if serializer.is_valid():
            day = serializer.validated_data["day"]

            # Utiliza get_or_create para buscar o crear el resultado
            result, created = Result.objects.get_or_create(
                day=day, defaults=serializer.validated_data
            )

            # Si el resultado ya existía, actualiza los campos con los nuevos datos
            if not created:
                serializer.update(result, serializer.validated_data)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_user(request):
    if request.method == "POST":
        serializer = AnimdleUserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]

            # Utiliza get_or_create para buscar o crear el usuario
            user, created = AnimdleUser.objects.get_or_create(
                username=username, defaults=serializer.validated_data
            )

            # Si el usuario ya existía, actualiza los campos con los nuevos datos
            if not created:
                serializer.update(user, serializer.validated_data)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
