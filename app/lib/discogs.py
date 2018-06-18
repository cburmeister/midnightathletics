import os

import requests

BASE_URL = 'https://api.discogs.com'
HEADERS = {
    'Accept': 'application/vnd.discogs.v2.html+json',
    'User-Agent': 'MidnightAthleticsRadio/0.0.1',
    'Authorization': 'Discogs token={}'.format(
        os.environ['DISCOGS_API_TOKEN']
    ),
}


def get_artist_data(artist_id):
    """Returns Discogs artist data for the given artist id."""
    data = []
    url = '{}/artists/{}'.format(BASE_URL, str(artist_id))
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    artist_data = response.json()
    data.append(artist_data)
    for member in artist_data.get('members', []):
        url = '{}/artists/{}'.format(BASE_URL, str(member['id']))
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        artist_data = response.json()
        data.append(artist_data)
    return data
