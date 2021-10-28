const player = new Plyr("#player", {
    "controls": [
        "play-large",
        "play",
        "mute",
        "volume",
        "airplay"
    ],
    "listeners": {
        // This is fired for both "play" and "pause" events
        play: function (event) {
            // If this is a "pause" let the default event handler fire
            if (player.playing) {
                return true;
            } else {
                // Reload the source
                player.source = {
                    type: "audio",
                    title: "Midnight Athletics Radio",
                    sources: [{
                        src: "https://radio.midnightathletics.com/stream.mp3",
                        type: "audio/mp3"
                    }]
                };
                // Play the audio when it's ready
                player.on('ready', event => {
                    player.play();
                });
                return false;  // Prevent the default "play" event handler
            }
        }
    }
});

function poll_icecast_status() {
    $("#now-playing").load("/now-playing");
}
poll_icecast_status();
setInterval(poll_icecast_status, 1000 * 300);  // 5 Minutes
