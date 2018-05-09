from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def root():
    title = 'Midnight Athletics Radio'
    description = (
        'Commercial free radio featuring contemporary underground dance '
        'music from around the world.'
    )
    return render_template('root.html', title=title, description=description)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
