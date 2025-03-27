#!/bin/bash

VENV_PATH="./venv"

function log() {
    echo -e "\033[1;32m$1\033[0m $(date +'(%H:%M:%S')) $2"
}

function install_dependencies() {
    log "installing dependencies"
    $VENV_PATH/bin/pip install -r dependencies.txt
}

if [ ! -x "$(command -v python)" ]; then
    log "python is not installed"
    exit 1
fi

if [ ! -d "$VENV_PATH" ]; then
    log "creating venv"
    python -m venv $VENV_PATH
    install_dependencies
fi

$VENV_PATH/bin/python .
