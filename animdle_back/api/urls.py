from django.urls import path

from api.views import create_anime, create_day, create_result, create_theme, create_user

urlpatterns = [
    path("api/create-anime/", create_anime, name="create-anime"),
    path("api/create-theme/", create_theme, name="create-theme"),
    path("api/create-day/", create_day, name="create-day"),
    path("api/create-result/", create_result, name="create-result"),
    path("api/create-user/", create_user, name="create-user"),
]
