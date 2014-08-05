#!/bin/bash

# creates virtual environment
# virtualenv env
# source env/bin/activate
# installs dependencies
pip install -r requirements.txt
# sets secret key for flask
key=`head -c 30 /dev/random | base64`
echo "app_secret_key = '$key'" >keys.py
# creates database
python model.py
# runs on localhost:5000
./run.sh
