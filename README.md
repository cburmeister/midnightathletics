midnightathletics
=================

Commercial free radio featuring contemporary underground dance music from around the world.

- https://midnightathletics.com/ - The project website/player
- https://radio.midnightathletics.com/ - The `Icecast` interface

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
| `LETSENCRYPT_EMAIL`       | Your email for use with Let's Encrypt.                        |
| `LIQUIDSOAP_DATA`         | An absolute path to a directory of audio files.               |
| `LIQUIDSOAP_HARBOR_PORT`  | Port used to connect when livestreaming.                      |
| `LIQUIDSOAP_VIRTUAL_HOST` | Hostname of the `liquidsoap` server. (used by `nginx-proxy`)  |
| `S3_ACCESS_KEY_ID`        | An AWS provisioned secret key id used to communicate with s3. |
| `S3_BUCKET_NAME`          | The name of the s3 bucket containing audio.                   |
| `S3_SECRET_ACCESS_KEY`    | An AWS provisioned secret key used to communicate with s3.    |
| `SECRET_KEY`              | A secret key required by the `app` to provide authentication. |
| `SENTRY_DSN`              | A secret required for logging exceptions with Sentry.         |

## Deployment

There are [Kustomizations](https://kustomize.io/) in the `kustomize` directory
suitable for deploying this with [Kubernetes](https://kubernetes.io/).

## Continuous Integration and Deployment

The configurations in this repository are built, tested and deployed via
[GitHub Actions](https://github.com/features/actions).
