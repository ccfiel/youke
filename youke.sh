#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
pkill python
source "$DIR/env/bin/activate"
git reset --hard
git pull
pip install -r requirements.txt
pip install --upgrade youtube_dl
python "$DIR/server.py" &
PID=$!

if [ -f /media/usb0/data.db ]; then
    rm /media/usb0/data.db
fi

while true; do
    sleep 120
    git fetch origin
    reslog=$(git log HEAD..origin/master --oneline)
    if [[ "${reslog}" != "" ]] ; then
        git merge origin/master
        kill -KILL $PID
        python "$DIR/server.py" &
        PID=$!
	fi
done
