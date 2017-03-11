import db
from threading import Thread
from db import kodi


class Player(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event
        self.kodi = kodi()

    def run(self):
        while not self.stopped.wait(2):
            if not self.is_playing():
                self.play_new_song()

            if self.is_finish_playing():
                self.stop_player()
                self.play_new_song()

    def is_finish_playing(self):
        result = self.kodi.Player.GetProperties(playerid=1, properties=["percentage"])
        if float(result['result']['percentage']) >= 98:
            return True
        else:
            return False

    def stop_player(self):
        self.kodi.Player.Stop(playerid=1)

    def play_new_song(self):
        song = db.play_next()
        if song:
            try:
                self.play_the_song(song)
            except:
               None
        elif db.is_working():
            try:
                song = db.next_alternative_song()
                if song:
                    self.play_the_song(song)
            except:
               None

    def play_the_song(self, play):
        self.kodi.VideoLibrary.Scan()
        result = self.kodi.Player.Open(item={"file": str(db.path() + play['title'] + ".mp4")})
        self.kodi.GUI.ShowNotification(title=play['title'], message="Now Playing", displaytime=20000)
        if 'error' in result:
            if play['error'] >= 20:
                db.update(play['youtube_id'], 'error', 0)
                db.update(play['youtube_id'], 'status', 'error')

            self.kodi.VideoLibrary.Scan()
            db.update(play['youtube_id'], 'error', play['error'] + 1)
        else:
            db.set_to_done()
            db.update(play['youtube_id'], 'status', 'playing')

    def play_current_song(self):
        if not self.is_playing():
            play = db.current_playing_song()
            if play:
                self.kodi.VideoLibrary.Scan()
                result = self.kodi.Player.Open(item={"file": str(db.path() + play['title'] + ".mp4")})
                self.kodi.GUI.ShowNotification(title=play['title'], message="Now Playing", displaytime=20000)
                if 'error' in result:
                    if play['error'] >= 20:
                        db.update(play['youtube_id'], 'error', 0)
                        db.update(play['youtube_id'], 'status', 'error')

                    self.kodi.VideoLibrary.Scan()
                    db.update(play['youtube_id'], 'error', play['error'] + 1)

    def is_playing(self):
        active = self.kodi.Player.GetActivePlayers()
        if active['result']:
            return True
        else:
            return False



