#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
python3 -m src.main configs/flask.yaml order
echo "pip install flask:"
echo "zipp markupsafe itsdangerous click blinker werkzeug jinja2 importlib-metadata flask"
