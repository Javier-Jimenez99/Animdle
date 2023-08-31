from django.urls import path, register_converter

from api.views import (
    create_anime,
    create_day,
    create_guest,
    create_theme,
    game_state,
    guess,
    todays_anime,
    todays_video,
)

from .converters import DateConverter, GameModeConverter

register_converter(GameModeConverter, "mode")
register_converter(DateConverter, "date")

urlpatterns = [
    path("create-anime/", create_anime, name="create-anime"),
    path("create-theme/", create_theme, name="create-theme"),
    path("create-day/", create_day, name="create-day"),
    path("create-guest/", create_guest, name="create-guest"),
    path("todays-anime/<mode:game_mode>/", todays_anime, name="todays-anime"),
    path("todays-video/<mode:game_mode>/", todays_video, name="todays-video"),
    # Date is optional, by default it will be now in Japan
    path("game-state/<mode:game_mode>/<date:date>/", game_state, name="game-state"),
    path("game-state/<mode:game_mode>/", game_state, name="game-state-today"),
    path("guess/<mode:game_mode>/<str:title>/", guess, name="guess-today"),
    path("guess/<mode:game_mode>/<str:title>/<date:date>/", guess, name="guess"),
]
