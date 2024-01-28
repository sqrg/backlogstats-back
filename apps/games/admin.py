from django.contrib import admin

from games.models import Game, CollectionGame


class GameAdmin(admin.ModelAdmin):
    pass


class CollectionGameAdmin(admin.ModelAdmin):
    pass


admin.site.register(Game, GameAdmin)
admin.site.register(CollectionGame, CollectionGameAdmin)
