from django.urls import path, register_converter

from api.views import create_guest, game_state, guess, todays_anime, todays_video

from .converters import DateConverter, GameModeConverter

register_converter(GameModeConverter, "mode")
register_converter(DateConverter, "date")

urlpatterns = [
    path("create-guest/", create_guest, name="create-guest"),
    path("todays-anime/<mode:game_mode>/", todays_anime, name="todays-anime"),
    path("todays-video/<mode:game_mode>/", todays_video, name="todays-video"),
    # Date is optional, by default it will be now in Japan
    path("game-state/<mode:game_mode>/<date:date>/", game_state, name="game-state"),
    path("game-state/<mode:game_mode>/", game_state, name="game-state-today"),
    path("guess/<mode:game_mode>/", guess, name="guess-today"),
    path("guess/<mode:game_mode>/<date:date>/", guess, name="guess"),
]
