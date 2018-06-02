import json

import youtube_dl


def download_mix(url, filename):
    """Downloads a mix from a URL and saves it with the given filename."""
    ydl_args = {'outtmpl': '/data/mixes/{}.%(ext)s'.format(filename)}
    with youtube_dl.YoutubeDL(ydl_args) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        filename = filename.split('/')[-1]
        return filename


def serialize_mix(row):
    """Returns a mix and its metadata as JSON."""
    discogs_artist_ids = [
        int(x.strip()) for x
        in str(row['discogs_artist_ids']).split(',') if x
    ]
    artist_data = row['artist_data']
    if artist_data:
        artist_data = json.loads(artist_data)
    return {
        'artist_data': artist_data,
        'discogs_artist_ids': discogs_artist_ids,
        'id': row['id'],
        'mixes_db_url': row['mixes_db_url'],
    }
