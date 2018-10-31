const player = new Plyr("#player", {
    "controls": ["play-large", "play", "mute", "volume", "airplay"],
});

function poll_icecast_status() {
    $("#now-playing").load("https://midnightathletics.com/now-playing");
}

poll_icecast_status();
setInterval(poll_icecast_status, 1000 * 300);  // 5 Minutes
