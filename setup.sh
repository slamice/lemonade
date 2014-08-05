#!/bin/bash -eux

# virtual environment
virtualenv env
source env/bin/activate
# install dependencies
pip install-r requirements.txt
# set flask secret key
key=`head -c 30 /dev/random | base64`
echo "app_secret_key = '$key'" >keys.py
# create database
python -i model.py
Base.metadata.create_all(engine)
quit()
# run the app
./run.sh