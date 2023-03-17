#!/bin/sh

# Define main script to be executed by Flask
export FLASK_APP=./source/index.py

# Run Flask application in the context of the virtual env listening to
# all interfaces on the computer

# Note: This is running in development mode, which grants us the hot reload feature.
pipenv run flask --debug run -h 0.0.0.0