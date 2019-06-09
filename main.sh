#!/bin/bash
export GOOGLE_APPLICATION_CREDENTIALS="/Users/nimish/Desktop/Angel/APP/credentials.json"
export FLASK_APP=run.py
node APP/index.js &
python TXTSIM/run.py

