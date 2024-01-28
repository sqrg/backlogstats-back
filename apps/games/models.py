from django.db import models

from igdb.models import Game, Platform
from profiles.models import Collection, List


class CollectionGame(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('PLAYING', 'Playing'),
        ('FINISHED', 'Finished'),
        ('ABANDONED', 'Abandoned'),
    ]

    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='NEW')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    platform = models.ForeignKey(
        Platform, on_delete=models.SET_NULL, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    lists = models.ManyToManyField(List, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.game.name} [{self.platform.name}]'


class Playthrough(models.Model):
    collection_game = models.ForeignKey(
        CollectionGame, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.game
