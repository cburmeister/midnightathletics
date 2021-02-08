FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8

ENV STATIC_INDEX 0

ENV LISTEN_PORT 5000
EXPOSE 5000

COPY . /app

RUN pip install -r /app/requirements.txt
