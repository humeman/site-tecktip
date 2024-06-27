#!/bin/bash

set -e
source ~/.profile

readonly NAME={{ site_name }}
readonly DOCROOT="/var/www/$NAME/api"

cd $DOCROOT

if [  ]

source venv/bin/activate
hypercorn app