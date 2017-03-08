from bottle import post, run, PasteServer
from bottle_rest import json_to_params
from threading import Event
from downloader import Downloader
from player import Player
from notify import Notify
from maintain import Maintain
import db
from db import kodi


from bottle import Bottle, ServerAdapter


class MyWSGIRefServer(ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server,  WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        # self.server.server_close() <--- alternative but causes bad fd exception
        self.server.shutdown()


app = Bottle()
server = MyWSGIRefServer(host='0.0.0.0', port=8000)


@post("/queue")
@json_to_params
def queue(id, title):
    if not db.is_exist(id):
        player = kodi()
        db.insert_data({"youtube_id": id, "title": title, "status": "idle"})
        player.GUI.ShowNotification(title=title, message="Successfully Queued", displaytime=20000)
        return "ok"
    else:
        return "already been in queue"


def run_server():
    db.init_data()
    db.load_to_file()

    player_event = Event()
    thread_player = Player(player_event)
    thread_player.play_current_song()
    thread_player.setDaemon(True)
    thread_player.start()

    down_event = Event()
    thread_down = Downloader(down_event)
    thread_down.setDaemon(True)
    thread_down.start()

    notify_event = Event()
    thread_notify = Notify(notify_event)
    thread_notify.setDaemon(True)
    thread_notify.start()

    maintain_event = Event()
    thread_maintain = Maintain(maintain_event)
    thread_maintain.setDaemon(True)
    thread_maintain.start()

    try:
        app.run(server=server)
    except Exception, ex:
        print ex
        # run(host='0.0.0.0', port=8000, server=PasteServer)

if __name__ == '__main__':
    run_server()
