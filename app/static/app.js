function poll_icecast_status() {
    $.getJSON("http://midnightathletics.com:8000/status-json.xsl", function(json){
        var source = json.icestats.source[0];
        $("#now-playing").text("Now playing: " + source.title);
        $("#num-listeners").text("Listeners: " + source.listeners);
    });
}
setInterval(poll_icecast_status, 5000);
