#!/usr/bin/liquidsoap

# Activate the telnet server
set('server.telnet', true)
set('server.telnet.bind_addr', '0.0.0.0')

# Activate the live stream input
set('harbor.bind_addr', '0.0.0.0')

# Begin the source by randomizing mixes from a directory
mixes = playlist(mode='random', '/data/mixes')

# Munge the audio file metadata to a somewhat standardized format
def update_metadata(m) =
    print('#{m}')
    title = m['filename']
    title = string.split(separator='/', title)
    title = list.nth(list.rev(title), 0)
    [('artist', ''), ('title', '#{title}')]
end

# ...and tell it to `update_metadata` when playing a new mix
mixes = map_metadata(strip=true, update_metadata, mixes)

# Add a server command that will skip the current audio file
def add_skip_command(s) =
    # A command to skip
    def skip(_) =
        source.skip(s)
        'Done!'
    end
    # Register the command
    server.register(
        namespace='#{source.id(s)}',
        usage='skip',
        description='Skip the current mix.',
        'skip',
        skip
    )
end
add_skip_command(mixes)

# Setup a source of queued up requests
requests = request.queue(id='request')

# ...and tell it to `update_metadata` when playing a new mix
requests = map_metadata(strip=true, update_metadata, requests)

# Configure the live input
live = input.harbor(
    'live',
    port=int_of_string(getenv('LIQUIDSOAP_HARBOR_PORT')),
    password=getenv('ICECAST_SOURCE_PASSWORD')
)

# Assemble the sources in order of priority
stream = fallback(track_sensitive=false, [live, requests, mixes])

# Stream the output in 192kpbs MP3
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
    url='http://radio.midnightathletics.com/stream.mp3',
    fallible=true
)

# Stream the output in 128kpbs AAC
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
    url='http://radio.midnightathletics.com/stream128.aac',
    fallible=true
)

# Stream the output in 64kpbs AAC
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
    url='http://radio.midnightathletics.com/stream64.aac',
    fallible=true
)

# Configure a live input for soundchecks
soundcheck = input.harbor(
    'soundcheck',
    port=int_of_string(getenv('LIQUIDSOAP_HARBOR_PORT_2')),
    password=getenv('ICECAST_SOURCE_PASSWORD')
)

# Stream the soundcheck output in 192kpbs MP3
output.icecast(
    %mp3(bitrate=192),
    soundcheck,
    host=getenv('ICECAST_HOST'),
    port=int_of_string(getenv('ICECAST_PORT')),
    password=getenv('ICECAST_SOURCE_PASSWORD'),
    mount='soundcheck.mp3',
    name='Soundcheck',
    fallible=true
)
