from __future__ import unicode_literals
from itertools import zip_longest
import json
import os
import telnetlib

from flask import Flask, abort, render_template
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from requests.status_codes import codes as status_codes
from flask_caching import Cache
import requests

from lib.discogs import get_artist_data
from lib.gsheet import get_google_sheet

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['CACHE_TYPE'] = 'filesystem'
app.config['CACHE_DIR'] = '/tmp'
app.config['CACHE_DEFAULT_TIMEOUT'] = 60 * 1

auth = HTTPBasicAuth()
cache = Cache(app)
CORS(app)

app.jinja_env.globals.update({
    'app_title': 'Midnight Athletics Radio',
    'app_description': (
        'Commercial free radio featuring contemporary underground dance '
        'music from around the world.'
    ),
    'app_url': 'https://midnightathletics.com/',
})


@auth.get_password
def get_pw(username):
    """Returns the password required for certain endpoints."""
    return os.environ['ICECAST_SOURCE_PASSWORD']


@app.route('/', methods=['GET'])
def root():

    # First attempt to get a cached response
    cache_key = 'now-playing'
    stats = cache.get(cache_key)
    if stats:
        payload = json.loads(stats)
        return render_template('root.html', data=payload)

    return render_template('root.html')


@app.route('/now-playing', methods=['GET'])
def now_playing():

    # First attempt to get a cached response
    cache_key = 'now-playing'
    stats = cache.get(cache_key)
    if stats:
        payload = json.loads(stats)
        return render_template('now-playing.html', data=payload)

    # Otherwise get the now playing title from icecast
    try:
        response = requests.get(
            os.environ['ICECAST_HOST'] + '/status-json.xsl'
        )
        response.raise_for_status()
    except Exception:
        abort(503)
    stats = response.json()

    # Begin building a payload for the response
    sources = stats['icestats']['source']
    payload = {
        'artist_data': [],
        'listeners': sum([x['listeners'] for x in sources]),
        'mixes_db_url': None,
        'title': sources[0]['title'],
    }

    # Get the now playing metadata from the google sheet
    sheet = get_google_sheet()
    try:
        cell = sheet.find(payload['title'])
        head = sheet.row_values(1)
        row_values = sheet.row_values(cell.row)
        row = dict(zip_longest(head, row_values, fillvalue=''))

        # Get artist metadata from Discogs
        artist_data = []
        artist_ids = [
            int(x.strip()) for x
            in str(row['discogs_artist_ids']).split(',') if x
        ]
        for artist_id in artist_ids:
            artist_data.extend(get_artist_data(artist_id))

        # Munge the audio file metadata to a somewhat standardized format
        title = sources[0]['title']
        title = ' '.join([x.title() for x in title.split('.')[:-1]])

        # Assemble a payload for the response
        payload.update({
            'artist_data': artist_data,
            'mixes_db_url': row['mixes_db_url'],
            'title': title,
        })

    except Exception:
        # If we get here there's a good chance someone is live streaming which
        # is why we don't have any metadata for what's "now playing"
        pass

    # Cache and return the new response
    cache.set(cache_key, json.dumps(payload))
    return (
        render_template('now-playing.html', data=payload),
        status_codes.OK
    )


@app.route('/skip', methods=['POST'])
@auth.login_required
def skip():

    # Send skip command to liquidsoap
    with telnetlib.Telnet(os.environ['LIQUIDSOAP_HOST'], 1234) as tn:
        tn.write(b'stream(dot)mp3.skip' + b'\n')

    # Bust the now playing cache
    cache_key = 'now-playing'
    cache.delete(cache_key)

    return 'Mix skipped.', status_codes.OK


@app.route('/request/<filename>', methods=['POST'])
@auth.login_required
def request_mix(filename):

    # Validate filename
    sheet = get_google_sheet()
    cell = sheet.find(filename)
    if not cell:
        return 'Mix not found.', status_codes.NOT_FOUND

    # Send skip command to liquidsoap
    with telnetlib.Telnet(os.environ['LIQUIDSOAP_HOST'], 1234) as tn:
        path = '/data/mixes/{}'.format(filename)
        tn.write('request.push {}'.format(path).encode() + b'\n')

    return 'Mix requested.', status_codes.OK


if __name__ == '__main__':
    app.run(host='0.0.0.0')
