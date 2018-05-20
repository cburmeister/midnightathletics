from __future__ import unicode_literals
import os

from flask import Flask, flash, render_template, request
from flask_httpauth import HTTPBasicAuth
import youtube_dl

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

auth = HTTPBasicAuth()


@auth.get_password
def get_pw(username):
    return os.environ['ICECAST_SOURCE_PASSWORD']


@app.route('/', methods=['GET'])
def root():
    title = 'Midnight Athletics Radio'
    description = (
        'Commercial free radio featuring contemporary underground dance '
        'music from around the world.'
    )
    return render_template('root.html', title=title, description=description)


@app.route('/upload', methods=['GET', 'POST'])
@auth.login_required
def upload():
    if request.method == 'POST':
        url = request.form.get('url')
        filename = request.form.get('filename')
        if not url or not filename:
            flash('URL and filename required.', category='danger')
        try:
            ydl_args = {
                'outtmpl': '{}/{}.%(ext)s'.format(
                    os.environ['LIQUIDSOAP_DATA'],
                    filename
                )
            }
            with youtube_dl.YoutubeDL(ydl_args) as ydl:
                ydl.download([url])
            flash('Uploaded {}'.format(filename), category='success')
        except youtube_dl.utils.DownloadError as e:
            flash(str(e), category='danger')
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
