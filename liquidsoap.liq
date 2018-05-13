#!/usr/bin/liquidsoap

set('harbor.bind_addr', '0.0.0.0')

mixes = playlist('/data/mixes')

def update_metadata(m) =
    print('#{m}')
    title = m['filename']
    title = string.split(separator='/', title)
    title = list.nth(list.rev(title), 0)
    title = string.split(separator='\.', title)
    extension = list.nth(list.rev(title), 0)
    title = list.remove(extension, title)
    title = list.map(string.capitalize, list.rev(title))
    title = string.concat(separator=' ', title)
    [('title', '#{title}')]
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
    url='http://midnightathletics.com:8000/stream.mp3',
    fallible=true
)

output.icecast(
    %aac(bitrate=128),
    stream,
    host=getenv('ICECAST_HOST'),
    port=int_of_string(getenv('ICECAST_PORT')),
    password=getenv('ICECAST_SOURCE_PASSWORD'),
    mount='stream128.aac',
    name='Midnight Athletics Radio',
    genre='House & Techno',
    description='Commercial free radio featuring contemporary underground dance music from around the world.',
    url='http://midnightathletics.com:8000/stream128.aac',
    fallible=true
)

output.icecast(
    %aac(bitrate=64),
    stream,
    host=getenv('ICECAST_HOST'),
    port=int_of_string(getenv('ICECAST_PORT')),
    password=getenv('ICECAST_SOURCE_PASSWORD'),
    mount='stream64.aac',
    name='Midnight Athletics Radio',
    genre='House & Techno',
    description='Commercial free radio featuring contemporary underground dance music from around the world.',
    url='http://midnightathletics.com:8000/stream64.aac',
    fallible=true
)
