const player = new Plyr("#player", {
    "controls": ["play-large", "play", "mute", "volume", "airplay"],
});

function poll_icecast_status() {
    $.getJSON("http://midnightathletics.com/now-playing", function(json) {
        $("#now-playing").text(json.title);
        $("#num-listeners").text("Listeners: " + json.listeners);
    });
}

poll_icecast_status();
setInterval(poll_icecast_status, 10000);
