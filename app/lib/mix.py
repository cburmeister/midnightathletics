import youtube_dl


def download_mix(url, filename):
    """Downloads a mix from a URL and saves it with the given filename."""
    ydl_args = {'outtmpl': '/data/mixes/{}.%(ext)s'.format(filename)}
    with youtube_dl.YoutubeDL(ydl_args) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        filename = filename.split('/')[-1]
        return filename
