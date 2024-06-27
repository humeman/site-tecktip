#!/bin/bash

set -e
source ~/.profile

readonly NAME={{ site_name }}
readonly DOCROOT="/var/www/$NAME"

nvm use {{ node_version }}

readonly VERSION=$(cat "$DOCROOT/repo/version")

cd "$DOCROOT/repo/$VERSION/src"
HOST="127.0.0.1" PORT={{ svelte_port }} node "$DOCROOT/repo/$VERSION/src/build/index.js"