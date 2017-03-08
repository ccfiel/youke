import db
from threading import Thread
from db import kodi


class Notify(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event
        self.kodi = kodi()

    def run(self):
        while not self.stopped.wait(60):
            show = False
            song = db.next_song()
            if song != 1:
                if song:
                    title = song['title']
                    message = "Next Song"
                    time = 20000
                    show = True
                else:
                    title = "Please Select Song"
                    message = "No Song queued"
                    time = 5000
                    active = self.kodi.Player.GetActivePlayers()
                    if active['result']:
                        show = True
                if show:
                    self.kodi.GUI.ShowNotification(title=title, message=message, displaytime=time)
