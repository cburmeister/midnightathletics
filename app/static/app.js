function poll_icecast_status() {
    $.getJSON("http://midnightathletics.com:8000/status-json.xsl", function(json){
        var source = json.icestats.source[0];
        var title = source.title;
        now_playing = title
            .substring(title.lastIndexOf("/") + 1)
            .replace(/\.[^/.]+$/, "")
            .replace(/\./g, " ")
            .split(" ")
            .map(function(v){return v.charAt(0).toUpperCase() + v.slice(1)})
            .join(" ");
        $("#now-playing").text("Now playing: " + now_playing);
        $("#num-listeners").text("Listeners: " + source.listeners);
    });
}
setInterval(poll_icecast_status, 5000);
