import pytube


# noinspection PyBroadException
def video_download(url, resolution):
    try:
        yt = pytube.YouTube(url)
        yt.streams.get_by_resolution(resolution).download()
        return {'Bool': True, 'Title': yt.title}
    except:
        return {'Bool': False}


# noinspection PyBroadException
def playlist_download(url, resolution):
    try:
        yt = pytube.Playlist(url)
        titles = list()
        for video in yt.videos:
            video.streams.get_by_resolution(resolution).download()
            titles.append(video.title)
        return {'Bool': True, 'Title': titles}
    except:
        return {'Bool': False}
