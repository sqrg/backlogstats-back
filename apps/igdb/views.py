from django.http import HttpResponse

from rest_framework import generics

from igdb.models import Genre, Platform

from igdb.serializers import GenreSerializer, PlatformSerializer

from services import igdb_service


class GenresList(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class PlatformsList(generics.ListAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


def update_genres(request):
    Genre.objects.all().delete()

    results = igdb_service.get_genres()

    if results is not None:
        genres = [Genre(**data) for data in results]
        Genre.objects.bulk_create(genres)

    return HttpResponse(status=200)


def update_platforms(request):
    Platform.objects.all().delete()

    results = igdb_service.get_platforms()

    if results is not None:
        platforms = [Platform(**data) for data in results]
        Platform.objects.bulk_create(platforms)

    return HttpResponse(status=200)
