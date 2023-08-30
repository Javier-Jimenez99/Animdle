from datetime import datetime as dt

import pytz
from rest_framework import status
from rest_framework.response import Response

from ..models import Anime, Day
from ..serializers import ThemeSerializer


def get_today_day():
    japan_date = dt.now(tz=pytz.timezone("Asia/Tokyo"))
    year = japan_date.year
    month = japan_date.month
    day = japan_date.day

    day_obj = Day.objects.get(date__year=year, date__month=month, date__day=day)

    return day_obj


def get_theme(game_mode, day_obj):
    if game_mode == "opening":
        theme_obj = day_obj.easy_opening
    elif game_mode == "hardcore-opening":
        theme_obj = day_obj.hardcore_opening
    elif game_mode == "ending":
        theme_obj = day_obj.easy_ending
    elif game_mode == "hardcore-ending":
        theme_obj = day_obj.hardcore_ending

    serializer = ThemeSerializer(theme_obj)

    return serializer.data


def check_game_mode(game_mode):
    if game_mode not in [
        "opening",
        "hardcore-opening",
        "ending",
        "hardcore-ending",
    ]:
        return Response(
            {"error": "Invalid game mode"}, status=status.HTTP_400_BAD_REQUEST
        )

    return game_mode


def get_all_synonyms_relations():
    anime_objs = Anime.objects.all()

    all_animes_relations = {}
    for anime in anime_objs:
        all_animes_relations[anime.title] = anime.title
        for synonim in eval(anime.synonyms):
            all_animes_relations[synonim] = anime.title

    return all_animes_relations


def get_all_titles():
    anime_objs = Anime.objects.all()

    all_titles = []
    for anime in anime_objs:
        all_titles.append(anime.title)
        for synonim in eval(anime.synonyms):
            all_titles.append(synonim)

    return all_titles
