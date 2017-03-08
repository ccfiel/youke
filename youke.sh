#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
source "$DIR/env/bin/activate"
git reset --hard
git pull
pip install -r requirements.txt
python "$DIR/server.py" &
PID=$!
echo "im here"
while true; do
    sleep 30
    echo "updating..."
    git fetch origin
    reslog=$(git log HEAD..origin/master --oneline)
    if [[ "${reslog}" != "" ]] ; then
        git merge origin/master
        kill -KILL $PID
        python "$DIR/server.py" &
        PID=$!
	fi
done

