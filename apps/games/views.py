from datetime import datetime
from django.db import transaction
from django.shortcuts import get_object_or_404, render

from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from games.models import CollectionGame
from igdb.models import Game, Platform, ReleaseDate
from profiles.models import Collection, List, UserProfile

from games.serializers import CollectionGameSerializer
from igdb.serializers import GameSerializer

from services import igdb_service


def index(request):
    user_profile = get_user_profile(request.user)

    collection = Collection.objects.get(profile=user_profile)
    collection_games = CollectionGame.objects.filter(collection=collection)
    lists = List.objects.filter(profile=user_profile)

    context = {
        'collection': collection_games,
        'lists': lists,
    }

    return render(request, 'games/index.html', context)


class SearchGames(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        query = request.query_params.get('q', '')
        results = igdb_service.search(query)

        if results is not None:
            return Response(results)
        else:
            return Response({'error': 'There was an error processing your request'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GameDetailView(APIView):
    def get(self, request, id, format=None):
        game = get_or_create_game(id)

        if game is not None:
            serialized_game = GameSerializer(game)
            return Response(serialized_game.data)
        else:
            return Response({'error': 'There was an error processing your request'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddGameToCollection(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user_profile = get_user_profile(request.user)
        game = get_or_create_game(request.data.get('game'))

        serialized = CollectionGameSerializer(data=request.data)
        if serialized.is_valid():
            self.get_or_create_collection_game(
                game, serialized.validated_data, user_profile)

            return Response(serialized.data, status=status.HTTP_201_CREATED)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def get_or_create_collection_game(self, game, validated_data, user_profile):
        collection, created = Collection.objects.get_or_create(
            profile=user_profile)
        game = CollectionGame.objects.get_or_create(
            game=game,
            collection=collection,
            defaults={key: value for key,
                      value in validated_data.items() if key != 'game'}
        )
        return game


class AddGameToList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user_profile = get_user_profile(request.user)
        collection_game = get_object_or_404(
            CollectionGame, pk=request.data.get('collection_game_id'))
        list = get_object_or_404(
            List, pk=request.data.get('list_id'))

        if list.profile != user_profile:
            return Response({'error': 'User does not own list'}, status=status.HTTP_400_BAD_REQUEST)

        if collection_game in list.games.all():
            return Response({'error': 'Game already on list'}, status=status.HTTP_400_BAD_REQUEST)

        self.add_game_to_list(collection_game, list)

        return Response(status=status.HTTP_201_CREATED)

    def add_game_to_list(self, collection_game, list):
        list.games.add(collection_game)
        list.save()


def get_user_profile(user):
    try:
        return UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        raise NotFound('User profile not found')


def get_or_create_game(game_id) -> Game:
    if not game_id:
        raise ValidationError('Game ID is required')

    game, created = Game.objects.get_or_create(
        id=game_id,
        defaults={'name': ''}
    )
    if created:
        game_details = fetch_game_details(game_id)

        game.name = game_details['name']
        game.thumbnail_url = game_details['cover']['url']
        game.cover_url = game_details['cover']['url'].replace(
            't_thumb', 't_cover_big')
        game.save()

        game.platforms.set(game_details['platforms'])
        game.genres.set(game_details['genres'])

        release_dates_objects = []
        for r in game_details['release_dates']:
            date = r.get('date', None)

            if date is not None:
                release_date = ReleaseDate.objects.create(
                    id=r['id'],
                    game=game,
                    date=datetime.fromtimestamp(r['date']),
                    platform=Platform.objects.get(pk=r['platform']),
                    region=r['region'],
                )

                release_dates_objects.append(release_date)

        # Not really sure why ignore_conflicts has to be set to True
        ReleaseDate.objects.bulk_create(
            release_dates_objects, ignore_conflicts=True)

    return game


def fetch_game_details(game_id):
    game_result = igdb_service.get_game_by_id(game_id)
    if not game_result:
        raise NotFound('Game not found in IGDB')

    return game_result[0]
