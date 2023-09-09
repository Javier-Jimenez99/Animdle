from api.views import (
    create_guest,
    game_state,
    guess,
    played_modes,
    results,
    todays_anime,
    todays_video,
)
from django.urls import path, register_converter

from .converters import DateConverter, GameModeConverter

register_converter(GameModeConverter, "mode")
register_converter(DateConverter, "date")

urlpatterns = [
    path("create-guest/", create_guest, name="create-guest"),
    path("todays-anime/<mode:game_mode>/", todays_anime, name="todays-anime"),
    path("todays-video/<mode:game_mode>/", todays_video, name="todays-video"),
    # Date is optional, by default it will be now in Japan
    path("game-state/<mode:game_mode>/", game_state, name="game-state-today"),
    path("game-state/<mode:game_mode>/<date:date>/", game_state, name="game-state"),
    path("guess/<mode:game_mode>/", guess, name="guess-today"),
    path("guess/<mode:game_mode>/<date:date>/", guess, name="guess-date"),
    path("guess/<mode:game_mode>/<int:max_lives>/", guess, name="gues-lives"),
    path(
        "guess/<mode:game_mode>/<date:date>/<int:max_lives>/",
        guess,
        name="guess-date-lives",
    ),
    path("results/<mode:game_mode>/", results, name="results-today"),
    path("results/<mode:game_mode>/<date:date>/", results, name="results"),
    path("played-modes/", played_modes, name="played-modes-today"),
    path("played-modes/<date:date>/", played_modes, name="played-modes"),
]
