#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
source "$DIR/env/bin/activate"
git reset --hard
git pull
pip install -r requirements.txt
python "$DIR/server.py" &
PID=$!
while true; do
    sleep 30
    git fetch origin
    reslog=$(git log HEAD..origin/master --oneline)
    if [[ "${reslog}" != "" ]] ; then
        git merge origin/master
        kill -KILL $PID
        python "$DIR/server.py" &
        PID=$!
	fi
done

