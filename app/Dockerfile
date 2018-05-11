FROM tiangolo/uwsgi-nginx-flask:python3.6

ENV STATIC_INDEX 1

COPY ./app/requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY . /app
