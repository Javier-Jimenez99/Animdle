from ..models import Anime, Day
from ..serializers import ThemeSerializer


def get_day_by_date(date):
    day_obj = Day.objects.get(
        date__year=date.year, date__month=date.month, date__day=date.day
    )

    return day_obj


def get_theme(game_mode, day_obj):
    theme_obj = getattr(day_obj, game_mode)

    serializer = ThemeSerializer(theme_obj)

    return serializer.data


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
