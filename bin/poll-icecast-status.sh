#!/bin/bash

# Get the configuration from the environment
source /root/midnightathletics/.env

# Get the stats from the server
url=http://midnightathletics.com:8000/status-json.xsl

# Pluck out the interesting values in the response
json=$(curl -s $url)
title=$(echo $json | jq '.icestats.source[0].title')
listeners=$(echo $json | jq '.icestats.source | map(.listeners) | add')

# Dump a line of the values suitable for a CSV
now_iso8601=$(date +%Y-%m-%dT%H:%M:%S%z)
row="\"$now_iso8601\", $title, $listeners"
echo $row >> $LIQUIDSOAP_DATA/history.csv
echo $row
