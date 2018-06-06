import os

import discogs_client


discogs_client = discogs_client.Client(
    'MidnightAthleticsRadio/0.0.1',
    user_token=os.environ['DISCOGS_API_TOKEN']
)


def get_artist_data(artist_id):
    """Returns Discogs artist data for the given artist id."""
    data = []
    artist = discogs_client.artist(artist_id)
    if not artist:
        return
    for artist in [artist] + artist.members:
        data.append(artist.data)
    return data
