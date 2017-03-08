#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
source "$DIR/env/bin/activate"
git pull
pip install -r requirements.txt
python "$DIR/youke.py"