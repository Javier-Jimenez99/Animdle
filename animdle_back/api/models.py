from django.contrib.auth.models import AbstractUser
from django.db import models


class Anime(models.Model):
    id = models.IntegerField(primary_key=True)
    rank = models.IntegerField()
    title = models.CharField(max_length=200)
    popularity_score = models.FloatField()
    quality_score = models.FloatField()
    year = models.IntegerField()
    season = models.CharField(max_length=100)
    synopsis = models.TextField()
    synonyms = models.CharField(max_length=1000)
    image_url = models.CharField(max_length=200)
    hardcore = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.year})"


class Theme(models.Model):
    id = models.IntegerField(primary_key=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    spoiler = models.BooleanField()
    nsfw = models.BooleanField()
    video_url = models.CharField(max_length=200)
    video_resolution = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.anime.title} - {self.title}"


class Day(models.Model):
    id = models.IntegerField(primary_key=True)
    easy_opening = models.ForeignKey(
        Theme, on_delete=models.CASCADE, related_name="easy_opening"
    )
    easy_ending = models.ForeignKey(
        Theme, on_delete=models.CASCADE, related_name="easy_ending"
    )
    hardcore_opening = models.ForeignKey(
        Theme, on_delete=models.CASCADE, related_name="hardcore_opening"
    )
    hardcore_ending = models.ForeignKey(
        Theme, on_delete=models.CASCADE, related_name="hardcore_ending"
    )
    date = models.DateField()

    def __str__(self):
        return f"{self.date}"


class AnimdleUser(AbstractUser):
    user_browser_id = models.CharField(
        max_length=100, verbose_name="User Browser ID", default=""
    )
    last_login = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(auto_now_add=True)


class Result(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    user = models.ForeignKey(AnimdleUser, on_delete=models.CASCADE)
    won = models.BooleanField()
    attempts = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
