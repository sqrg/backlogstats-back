from django.conf import settings

import requests

BASE_URL = 'https://api.igdb.com/v4'


def build_headers():
    return {
        'Content-Type': 'text/plain',
        'Client-ID': settings.IGDB_API_CLIENT_ID,
        'Authorization': f'Bearer {settings.IGDB_API_ACCESS_TOKEN}',
    }


def get_genres():
    url = BASE_URL + '/genres'
    headers = build_headers()
    payload = 'fields id,name; limit 200;'
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_platforms():
    url = BASE_URL + '/platforms'
    headers = build_headers()
    payload = 'fields id,name,abbreviation; limit 200;'
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def search(query):
    url = BASE_URL + '/games'
    headers = build_headers()
    payload = f'search "{query}"; fields id,name;'
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_game_by_id(id: int):
    url = BASE_URL + '/games'
    headers = build_headers()
    payload = (
        'fields '
        'name,cover.url,platforms,genres,'
        'release_dates.date,release_dates.platform,release_dates.region;'
        f'where id = {id};'
    )

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return None
