#!/bin/bash

export FLASK_APP=./src
export FLASK_ENV=development
export YOURAPPLICATION_SETTINGS=config.py
source $(pipenv --venv)/bin/activate
flask run -h 0.0.0.0