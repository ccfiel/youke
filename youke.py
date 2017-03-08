from server import run_server
import subprocess
import sys
import os
import time
from threading import Thread
import os
import argparse
import signal
import daemon
import lockfile
import bottle
from contextlib import contextmanager

PIDFILE_PATH = "/tmp/website-builder.pid"
LOGFILE = "/tmp/website-builder.log"


def restart_program():
    sys.stderr.close()
    time.sleep(30)
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


@contextmanager
def __locked_pidfile(filename):
    # Acquire the lockfile
    lock = lockfile.FileLock(filename)
    lock.acquire(-1)

    # Write out our pid
    realfile = open(filename, "w")
    realfile.write(str(os.getpid()))
    realfile.close()

    # Yield to the daemon
    yield

    # Cleanup after ourselves
    os.remove(filename)
    lock.release()


def daemon_run(host="localhost", port="8080", ):
    """
    Get the bottle 'run' function running in the background as a daemonized
    process.

    :host: The host interface to listen for connections on. Enter 0.0.0.0
           to listen on all interfaces. Defaults to localhost.
    :port: The host port to listen on. Defaults to 8080.
    :pidfile: The file to use as the process id file. Defaults to "bottle.pid"
    :logfile: The file to log stdout and stderr from bottle to. Defaults to "bottle.log"

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "stop"])
    args = parser.parse_args()


    if args.action == "start":
            bottle.run(host=host, port=port)
    else:
        with open(pidfile, "r") as p:
            pid = int(p.read())
            os.kill(pid, signal.SIGTERM)


def run():
    pidfile = None
    logfile = None
    if pidfile is None:
        pidfile = os.path.join(
            os.getcwd(),
            "bottle.pid"
        )

    if logfile is None:
        logfile = os.path.join(
            os.getcwd(),
            "bottle.log"
        )

    log = open(logfile, "w+")
    context = daemon.DaemonContext(
        pidfile=__locked_pidfile(pidfile),
        stdout=log,
        stderr=log
    )

    with context:
        run_server()


if __name__ == '__main__':
    t = Thread(target=check_update)
    t.setDaemon(True)
    t.start()
    daemon_run()

