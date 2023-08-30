from django.urls import path

from api.views import (
    create_anime,
    create_day,
    create_guest,
    create_theme,
    game_state,
    todays_anime,
    todays_video,
)

urlpatterns = [
    path("create-anime/", create_anime, name="create-anime"),
    path("create-theme/", create_theme, name="create-theme"),
    path("create-day/", create_day, name="create-day"),
    path("create-guest/", create_guest, name="create-guest"),
    path("todays-anime/<str:game_mode>", todays_anime, name="todays-anime"),
    path("todays-video/<str:game_mode>", todays_video, name="todays-video"),
    # Date is optional, by default it will be now in Japan
    path("game-state/<str:game_mode>/<str:date>", game_state, name="game-state"),
    path("game-state/<str:game_mode>", game_state, name="game-state-today"),
]
