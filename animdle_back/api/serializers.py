from rest_framework import serializers

from .models import AnimdleUser, Anime, Day, Result, Theme


class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = "__all__"


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = "__all__"


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = "__all__"


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = "__all__"


class AnimdleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimdleUser
        fields = "__all__"
