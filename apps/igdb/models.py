from django.db import models


class Genre(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Platform(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Game(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    thumbnail_url = models.URLField(null=True, blank=True)
    cover_url = models.URLField(null=True, blank=True)
    platforms = models.ManyToManyField(Platform, related_name='games')
    genres = models.ManyToManyField(Genre, related_name='games')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class ReleaseDate(models.Model):
    class Region(models.IntegerChoices):
        EUROPE = 1
        NORTH_AMERICA = 2
        AUSTRALIA = 3
        NEW_ZEALAND = 4
        JAPAN = 5
        CHINA = 6
        ASIA = 7
        WORLDWIDE = 8
        KOREA = 9
        BRAZIL = 10

    id = models.PositiveIntegerField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date = models.DateTimeField()
    platform = models.ForeignKey(
        Platform, on_delete=models.SET_NULL, null=True)
    region = models.IntegerField(choices=Region.choices)

    def __str__(self) -> str:
        return f'{self.date} ({self.platform})'
