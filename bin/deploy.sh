#!/bin/bash

# Set timezone to PDT
rm /etc/localtime
ln -s /usr/share/zoneinfo/America/Los_Angeles /etc/localtime

# Get the configuration from the environment
source .env

# Plug in necessary values into the configuration files
if [ -n "$ICECAST_ADMIN_PASSWORD" ]; then
    KEY="admin-password"
    sed -i "s/<$KEY>[^<]*<\/$KEY>/<$KEY>$ICECAST_ADMIN_PASSWORD<\/$KEY>/g" icecast.xml
fi
if [ -n "$ICECAST_PASSWORD" ]; then
    KEY="password"
    sed -i "s/<$KEY>[^<]*<\/$KEY>/<$KEY>$ICECAST_PASSWORD<\/$KEY>/g" icecast.xml
fi
if [ -n "$ICECAST_RELAY_PASSWORD" ]; then
    KEY="relay-password"
    sed -i "s/<$KEY>[^<]*<\/$KEY>/<$KEY>$ICECAST_RELAY_PASSWORD<\/$KEY>/g" icecast.xml
fi
if [ -n "$ICECAST_SOURCE_PASSWORD" ]; then
    KEY="source-password"
    sed -i "s/<$KEY>[^<]*<\/$KEY>/<$KEY>$ICECAST_SOURCE_PASSWORD<\/$KEY>/g" icecast.xml
fi

# Recycle the docker compose services
docker-compose build
docker-compose stop
docker-compose rm --force
docker-compose up -d --no-recreate

# Set the crontab
crontab < /root/midnightathletics/bin/crontab.txt

# Tail the logs to ensure everything booted up correctly
docker-compose logs -f
