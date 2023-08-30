from django.urls import path

from api.views import (
    create_anime,
    create_day,
    create_guest,
    create_result,
    create_theme,
    todays_anime,
    todays_video,
)

urlpatterns = [
    path("create-anime/", create_anime, name="create-anime"),
    path("create-theme/", create_theme, name="create-theme"),
    path("create-day/", create_day, name="create-day"),
    path("create-result/", create_result, name="create-result"),
    path("create-guest/", create_guest, name="create-user"),
    path("todays-anime/<str:game_mode>", todays_anime, name="todays-anime"),
    path("todays-video/<str:game_mode>", todays_video, name="todays-video"),
]
