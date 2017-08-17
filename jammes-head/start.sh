#!/usr/bin/env bash

HERE=$(pwd)/$(dirname "$0")
PYTHON3="/usr/local/bin/python3"
SCRIPT="$HERE/JammesHead.py"

export PYTHONPATH="$PYTHONPATH:$HERE/.."

$PYTHON3 $SCRIPT