from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.models import AnimdleUser, Anime, Day, Theme


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AnimdleUser.objects.create_user(
            username="testuser", password="testpass"
        )
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Create animes
        anime = Anime.objects.create(
            id=1,
            rank=1,
            title="test",
            popularity_score=1.0,
            quality_score=1.0,
            year=2021,
            season="test",
            synopsis="test",
            synonyms="['test']",
            image_url="https://www.google.com",
            hardcore=False,
        )
        anime.save()

        # Create themes
        theme = Theme.objects.create(
            id=1,
            anime=anime,
            title="test",
            type="OP",
            spoiler=False,
            nsfw=False,
            video_url="https://www.youtube.com/watch?v=1",
            video_resolution=1080,
        )
        theme.save()

        # Create days
        day = Day.objects.create(
            id=1,
            easy_opening=theme,
            easy_ending=theme,
            hardcore_opening=theme,
            hardcore_ending=theme,
            date=datetime.now().date(),
        )
        day.save()

    def test_create_anime(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        data = {
            "id": 2,
            "rank": 1,
            "title": "test",
            "popularity_score": 1.0,
            "quality_score": 1.0,
            "year": 2021,
            "season": "test",
            "synopsis": "test",
            "synonyms": "['test']",
            "image_url": "https://www.google.com",
            "hardcore": False,
        }
        response = self.client.post(reverse("create-anime"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_theme(self):
        data = {
            "id": 2,
            "anime": 1,
            "title": "test",
            "type": "OP",
            "spoiler": False,
            "nsfw": False,
            "video_url": "https://www.youtube.com/watch?v=1",
            "video_resolution": 1080,
        }
        response = self.client.post(reverse("create-theme"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_day(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        data = {
            "id": 2,
            "easy_opening": 1,
            "easy_ending": 1,
            "hardcore_opening": 1,
            "hardcore_ending": 1,
            "date": datetime.now().date(),
        }
        response = self.client.post(reverse("create-day"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_guest(self):
        data = {}
        response = self.client.post(reverse("create-guest"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_todays_anime(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        game_mode = "opening"  # Modificar según corresponda
        response = self.client.get(
            reverse("todays-anime", args=[game_mode]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_todays_video(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        game_mode = "opening"  # Modificar según corresponda
        response = self.client.get(
            reverse("todays-video", args=[game_mode]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_game_state(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        game_mode = "opening"  # Modificar según corresponda
        response = self.client.get(
            reverse("game-state-today", args=[game_mode]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_game_state_custom_date(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        game_mode = "opening"  # Modificar según corresponda
        custom_date = (
            datetime.now().date().strftime("%Y-%m-%d")
        )  # Modificar según corresponda
        response = self.client.get(
            reverse("game-state", args=[game_mode, custom_date]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
