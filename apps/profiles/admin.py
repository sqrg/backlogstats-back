from django.contrib import admin

from profiles.models import UserProfile, Collection, List


class UserProfileAdmin(admin.ModelAdmin):
    pass


class CollectionAdmin(admin.ModelAdmin):
    pass


class ListAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(List, ListAdmin)
