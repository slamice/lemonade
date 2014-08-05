#!/bin/bash -eux
virtualenv env
source env/bin/activate
pip install -r requirements.txt
key=`head -c 30 /dev/random | base64`
echo "app_secret_key = '$key'" >keys.py
python -i model.py
Base.metadata.create_all(engine)
quit()
./run.sh
