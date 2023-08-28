from django.contrib import admin

from .models import AnimdleUser, Anime, Day, Result, Theme

admin.site.register(Anime)
admin.site.register(Theme)
admin.site.register(Day)
admin.site.register(AnimdleUser)
admin.site.register(Result)
