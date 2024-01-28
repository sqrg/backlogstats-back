from django.contrib import admin

from igdb.models import Genre, Platform, ReleaseDate


class GenreAdmin(admin.ModelAdmin):
    pass


class PlatformAdmin(admin.ModelAdmin):
    pass


class ReleaseDateAdmin(admin.ModelAdmin):
    pass


admin.site.register(Genre, GenreAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(ReleaseDate, ReleaseDateAdmin)
