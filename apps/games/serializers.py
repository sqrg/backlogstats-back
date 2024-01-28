from rest_framework import serializers

from games.models import CollectionGame
from igdb.models import Game, Platform


class CollectionGameSerializer(serializers.ModelSerializer):
    game = serializers.PrimaryKeyRelatedField(
        queryset=Game.objects.all())
    platform = serializers.PrimaryKeyRelatedField(
        queryset=Platform.objects.all(), allow_null=True)

    class Meta:
        model = CollectionGame
        fields = ['game', 'platform',
                  'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
