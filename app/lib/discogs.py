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


def clean_artist_urls(urls):
    """Clean artist URLs."""
    title_by_pattern = {
        'bandcamp': 'Bandcamp',
        'discogs': 'Discogs',
        'facebook': 'Facebook',
        'google': 'Google',
        'instagram': 'Instagram',
        'mixcloud': 'Mixcloud',
        'myspace': 'MySpace',
        'residentadvisor': 'Resident Advisor',
        'reverbnation': 'Reverb',
        'songkick': 'Songkick',
        'soundcloud': 'Soundcloud',
        'tumblr': 'Tumblr',
        'twitter': 'Twitter',
        'wikipedia': 'Wikipedia',
        'youtube': 'YouTube',
    }
    clean_urls = {}
    for url in urls:
        title = url
        title = title.replace('http://', '')
        title = title.replace('https://', '')
        for pattern in title_by_pattern.keys():
            if pattern in url:
                title = title_by_pattern.get(pattern)
        clean_urls[title] = url
    return clean_urls


def get_artist_data(artist_id):
    """Returns Discogs artist data for the given artist id."""
    data = []
    url = '{}/artists/{}'.format(BASE_URL, str(artist_id))
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    artist_data = response.json()
    artist_data['urls'] = clean_artist_urls(artist_data.get('urls', []))
    data.append(artist_data)
    return data
