midnightathletics
=================

Commercial free radio featuring contemporary underground dance music from around the world.

## Configuration

The following environment variables are *required*:

| Name                      | Purpose                                                       |
|---------------------------|---------------------------------------------------------------|
| `APP_VIRTUAL_HOST`        | Hostname of the `app` server. (used by `nginx-proxy`)         |
| `DISCOGS_API_TOKEN`       | An API token used to communicate with the Discogs API.        |
| `ICECAST_ADMIN_PASSWORD`  | Used for administration functions.                            |
| `ICECAST_PASSWORD`        | Used for administration functions.                            |
| `ICECAST_RELAY_PASSWORD`  | Used when a slave requests the list of streams to relay.      |
| `ICECAST_SOURCE_PASSWORD` | Used by sources to connect to `icecast`.                      |
| `ICECAST_VIRTUAL_HOST`    | Hostname of the `icecast` server. (used by `nginx-proxy`)     |
| `LIQUIDSOAP_DATA`         | An absolute path to a directory of audio files.               |
| `LIQUIDSOAP_HARBOR_PORT`  | Port used to connect when livestreaming.                      |
| `LIQUIDSOAP_VIRTUAL_HOST` | Hostname of the `liquidsoap` server. (used by `nginx-proxy`)  |
| `S3_ACCESS_KEY_ID`        | An AWS provisioned secret key id used to communicate with s3. |
| `S3_SECRET_ACCESS_KEY`    | An AWS provisioned secret key used to communicate with s3.    |
| `SECRET_KEY`              | A secret key required by the `app` to provide authentication. |
