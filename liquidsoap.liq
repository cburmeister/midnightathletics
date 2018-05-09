#!/usr/bin/liquidsoap

set('harbor.bind_addr', '0.0.0.0')

mixes = playlist('/data/mixes')

def update_metadata(m) =
    filename = m["filename"]
    print("#{m}")
    [("title", "#{filename}")]
end

mixes = map_metadata(update_metadata, mixes)

live = input.harbor(
    'live',
    port=int_of_string(getenv('LIQUIDSOAP_HARBOR_PORT')),
    password=getenv('ICECAST_SOURCE_PASSWORD')
)

stream = fallback(track_sensitive=false, [live, mixes])

output.icecast(
    %mp3(bitrate=192),
    stream,
    host=getenv('ICECAST_HOST'),
    port=int_of_string(getenv('ICECAST_PORT')),
    password=getenv('ICECAST_SOURCE_PASSWORD'),
    mount='stream.mp3',
    name='Midnight Athletics Radio',
    genre='House & Techno',
    description='Commercial free radio featuring contemporary underground dance music from around the world.',
    url='https://midnightathletics.com/',
    fallible=true
)

output.icecast(
    %mp3(bitrate=128),
    stream,
    host=getenv('ICECAST_HOST'),
    port=int_of_string(getenv('ICECAST_PORT')),
    password=getenv('ICECAST_SOURCE_PASSWORD'),
    mount='stream128.mp3',
    name='Midnight Athletics Radio',
    genre='House & Techno',
    description='Commercial free radio featuring contemporary underground dance music from around the world.',
    url='https://midnightathletics.com/',
    fallible=true
)
