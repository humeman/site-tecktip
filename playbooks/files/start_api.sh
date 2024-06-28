#!/bin/bash

set -e
source ~/.profile

readonly NAME={{ site_name }}
readonly DOCROOT="/var/www/$NAME/api"

cd $DOCROOT

if ! [ -d venv ]; then
    python{{ dependency_versions[env]["python"] }} -m venv venv
fi

source venv/bin/activate
pip3 install -r requirements.txt
python3 main.py