const player = new Plyr("#player", {
    "controls": ["play-large", "play", "mute", "volume", "airplay"],
});

function poll_icecast_status() {
    $.getJSON("http://radio.midnightathletics.com/status-json.xsl", function(json) {
        var listeners = 0;
        $.each(json.icestats.source, function(i, source){
            listeners = listeners + source.listeners;
        });
        $("#now-playing").text(json.icestats.source[0].title);
        $("#num-listeners").text("Listeners: " + listeners);
    });
}

poll_icecast_status();

setInterval(poll_icecast_status, 5000);
