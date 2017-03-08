import pafy
import db
import re
import os
from threading import Thread


class Downloader(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(0.5):
            for download in db.to_download():
                try:
                    db.update(download['youtube_id'], 'status', 'downloading')
                    info = get_video_info(download['youtube_id'])
                    name = strip_title(info.title)
                    db.update(download['youtube_id'], 'title', name)
                    db.update(download['youtube_id'], 'error', 0)
                    db.update(download['youtube_id'], 'duration', info.duration)
                    if not db.is_video_exists(name):
                        youtube_downloader(download['youtube_id'])
                        rename_song(info.title)
                    db.update(download['youtube_id'], 'status', 'cache')
                except:
                    None


def strip_title(title):
    name = re.sub(r'[^\w\-]+', ' ', title)
    name = name.strip()
    return name


def rename_song(title):
    name = strip_title(title)
    os.rename(db.path() + title + ".mp4", db.path() + name + ".mp4")
    return name


def get_video_info(youtube_id):
    url = "https://www.youtube.com/watch?v=" + youtube_id
    video = pafy.new(url)
    return video


def youtube_downloader(youtube_id):
    url = "https://www.youtube.com/watch?v=" + youtube_id
    video = pafy.new(url)

    all_streams = video.streams
    for s in all_streams:
        if s.extension == "mp4":
            s.download(filepath=db.path(), quiet=False)
            return video

