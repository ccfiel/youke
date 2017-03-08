import db
from threading import Thread
from os import listdir
from os.path import isfile, join
from db import path


class Maintain(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event
        self.files = [f for f in listdir(path()) if isfile(join(path(), f))]

    def run(self):
        while not self.stopped.wait(20):
            self.set_status_to_cache()
            db.save_to_file()

    def set_status_to_cache(self):
        for song in db.song_downloading():
            for file_name in self.files:
                if str(file_name).strip() == str(song['title'] + '.mp4').strip():
                    db.update(song['youtube_id'], 'status', 'cache')
                    break

