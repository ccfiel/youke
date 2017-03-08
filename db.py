from kodipydent import Kodi
import os
import pickle

path_str = "/media/usb0/Videoke/"
kodi_ip = '127.0.0.1'


def init_data():
    global data
    data = []


def insert_data(values):
    global data
    data.append(values)


def is_exist(youtube_id):
    global data
    if data:
        for curr in data:
            if curr['youtube_id'] == youtube_id:
                return curr
    return None


def to_download():
    global data
    output = []
    if data:
        for curr in data:
            if curr['status'] == 'idle':
                output.append(curr)
    return output


def song_downloading():
    global data
    output = []
    if data:
        for curr in data:
            if curr['status'] == 'downloading':
                output.append(curr)
    return output


def update(youtube_id, key, value):
    global data
    for index, element in enumerate(data):
        if element['youtube_id'] == youtube_id:
            data[index][key] = value


def display():
    global data
    if data:
        for curr in data:
            print curr


def play_next():
    global data
    for curr in data:
        if curr['status'] == 'cache':
            return curr

    return None


def next_song():
    global data
    if data:
        for curr in data:
            if str(curr['status']) == "cache" or str(curr['status']) == "downloading":
                return curr
        return None
    else:
        return 1


def current_playing_song():
    global data
    for curr in data:
        if str(curr['status']) == "playing":
            return curr
    return None


def set_to_done():
    global data
    for index, element in enumerate(data):
        if element['status'] == 'playing':
            data[index]['status'] = 'done'


def path():
    return path_str


def kodi():
    return Kodi(kodi_ip)


def is_video_exists(title):
    return os.path.isfile(path_str + title + ".mp4")


def save_to_file():
    global data
    if data:
        with open(path_str + 'data.db', 'wb') as fp:
            pickle.dump(data, fp)


def load_to_file():
    global data
    if os.path.isfile(path_str + 'data.db'):
        with open(path_str + 'data.db', 'rb') as fp:
            data = pickle.load(fp)



