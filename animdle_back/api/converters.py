from datetime import datetime as dt

import pytz


class GameModeConverter:
    regex = r"(opening)|(hardcore-opening)|(ending)|(hardcore-ending)"

    def to_python(self, value):
        return value.replace("-", "_")

    def to_url(self, value):
        return value


class DateConverter:
    regex = r"(\d{4}-\d{2}-\d{2})|(today)"

    def to_python(self, value):
        if value == "today":
            return dt.now(tz=pytz.timezone("Asia/Tokyo")).date()
        else:
            return dt.strptime(value, "%Y-%m-%d").date()

    def to_url(self, value):
        if value == "today":
            return dt.now(tz=pytz.timezone("Asia/Tokyo")).strftime("%Y-%m-%d")
        else:
            return value
