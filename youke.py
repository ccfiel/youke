from server import run_server
from server import server
import subprocess
import sys
import os
import time
from threading import Thread


def restart_program():
    server.stop()
    python = sys.executable
    os.execl(python, python, *sys.argv)


def update_app():
    try:
        subprocess.check_output(["git", "reset", "--hard"])
        output = subprocess.check_output(["git", "pull"])
        subprocess.check_output(["pip", "install", "-r", "requirements.txt"])
    except:
        output = 'up-to-date'

    if "up-to-date" in output:
        return True
    else:
        return False


def check_update():
    while True:
        if not update_app():
            restart_program()
        time.sleep(30)


if __name__ == '__main__':
    t = Thread(target=check_update)
    t.setDaemon(True)
    t.start()
    run_server()

