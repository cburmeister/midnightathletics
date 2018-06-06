from __future__ import unicode_literals
from itertools import zip_longest
import json
import os
import telnetlib

from flask import Flask, abort, flash, render_template, request, jsonify
from flask_httpauth import HTTPBasicAuth
from requests.status_codes import codes as status_codes

from lib.discogs import get_artist_data
from lib.gsheet import get_google_sheet
from lib.mix import download_mix, serialize_mix
from lib.s3 import upload_file_to_s3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

app.jinja_env.globals.update({
    'app_title': 'Midnight Athletics Radio',
    'app_description': (
        'Commercial free radio featuring contemporary underground dance '
        'music from around the world.'
    ),
    'app_url': 'http://midnightathletics.com/',
})

auth = HTTPBasicAuth()


@auth.get_password
def get_pw(username):
    """Returns the password required for certain endpoints."""
    return os.environ['ICECAST_SOURCE_PASSWORD']


@app.route('/', methods=['GET'])
def root():
    return render_template('root.html')


@app.route('/mixes', methods=['GET'])
@auth.login_required
def mixes():
    sheet = get_google_sheet()
    payload = [x['id'] for x in sheet.get_all_records()]
    return jsonify(payload), status_codes.OK


@app.route('/mixes/<id>', methods=['GET'])
@auth.login_required
def get_mix(id):
    sheet = get_google_sheet()
    cell = sheet.find(id)
    if not cell:
        abort(404)
    head = sheet.row_values(1)
    row_values = sheet.row_values(cell.row)
    row = dict(zip_longest(head, row_values, fillvalue=''))
    payload = serialize_mix(row)
    return jsonify(payload), status_codes.OK


@app.route('/upload', methods=['GET', 'POST'])
@auth.login_required
def upload():
    if request.method == 'POST':
        url = request.form.get('url')
        filename = request.form.get('filename')
        if not url or not filename:
            flash('URL and filename required.', category='danger')
        try:

            # Download mix using youtube-dl
            filename = download_mix(url, filename)

            # Gather artist data from Discogs
            discogs_artist_ids = [
                int(x.strip()) for x
                in request.form.get('discogs_artist_ids').split(',')
            ]
            artist_data = []
            for artist_id in discogs_artist_ids:
                artist_data.extend(get_artist_data(artist_id))

            # Log the mix in the google sheet
            sheet = get_google_sheet()
            sheet.append_row([
                filename,
                request.form.get('discogs_artist_ids'),
                request.form.get('mixes_db_url'),
                json.dumps(artist_data),
            ])

            # Ship it to s3 for safekeeping
            upload_file_to_s3('/data/mixes/' + filename, filename)

            flash('Uploaded {}'.format(filename), category='success')
        except Exception as e:
            flash(str(e), category='danger')
    return render_template('upload.html')


@app.route('/skip', methods=['POST'])
@auth.login_required
def skip():
    with telnetlib.Telnet('liquidsoap', 1234) as tn:
        tn.write(b'stream(dot)mp3.skip' + b'\n')
    return 'Mix skipped.', status_codes.OK


if __name__ == '__main__':
    app.run(host='0.0.0.0')
