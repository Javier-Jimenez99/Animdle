import datetime
from datetime import datetime as dt

import pytz
from api.models import AnimdleUser, Anime, Day, Result, Theme
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


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
        anime1 = Anime.objects.create(
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
        anime1.save()

        anime2 = Anime.objects.create(
            id=2,
            rank=2,
            title="test2",
            popularity_score=1.0,
            quality_score=1.0,
            year=2021,
            season="test",
            synopsis="test",
            synonyms="[]",
            image_url="https://www.google.com",
            hardcore=False,
        )
        anime2.save()

        # Create themes
        theme = Theme.objects.create(
            id=1,
            anime=anime1,
            title="test",
            type="OP",
            spoiler=False,
            nsfw=False,
            video_url="https://www.youtube.com/watch?v=1",
            video_resolution=1080,
        )
        theme.save()

        self.today_date = dt.now(tz=pytz.timezone("Asia/Tokyo")).date()
        # Create days
        day = Day.objects.create(
            id=1,
            opening=theme,
            ending=theme,
            hardcore_opening=theme,
            hardcore_ending=theme,
            date=self.today_date,
        )
        day.save()

        # Create results
        self.result = Result.objects.create(
            user=self.user, day=day, game_mode="opening"
        )

        day = Day.objects.create(
            id=2,
            opening=theme,
            ending=theme,
            hardcore_opening=theme,
            hardcore_ending=theme,
            date=self.today_date + datetime.timedelta(days=1),
        )
        day.save()

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
        game_mode = "hardcore-opening"  # Modificar según corresponda
        custom_date = self.today_date.strftime(
            "%Y-%m-%d"
        )  # Modificar según corresponda

        response = self.client.get(
            reverse("game-state", args=[game_mode, custom_date]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        date = (self.today_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        response = self.client.get(
            reverse("game-state", args=[game_mode, date]), format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "You can't play in the future")

    def test_guess_win(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        game_mode = "opening"  # Modificar según corresponda
        title = "test"
        date = self.today_date.strftime("%Y-%m-%d")

        response = self.client.post(
            reverse("guess", args=[game_mode, date]),
            data={"title": title},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["attempts"], ["test"])
        self.assertEqual(response.data["state"], "win")

        date = (self.today_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        response = self.client.post(
            reverse("guess", args=[game_mode, date]),
            data={"title": title},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "You can't play in the future")

    def test_guess_lose(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        game_mode = "opening"
        title = "test2"
        date = self.today_date.strftime("%Y-%m-%d")

        for i in range(1, 5):
            response = self.client.post(
                reverse("guess", args=[game_mode, date]),
                data={"title": title},
                format="json",
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["attempts"], ["test2"] * i)
            if i == 5:
                self.assertEqual(response.data["state"], "lose")
            else:
                self.assertEqual(response.data["state"], "pending")

    def test_results(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        game_mode = "opening"

        date = self.today_date.strftime("%Y-%m-%d")
        response = self.client.get(
            reverse("results", args=[game_mode, date]), format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        title = "test2"

        for i in range(5):
            response = self.client.post(
                reverse("guess", args=[game_mode, date]),
                data={"title": title},
                format="json",
            )

        response = self.client.get(
            reverse("results", args=[game_mode, date]), format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
