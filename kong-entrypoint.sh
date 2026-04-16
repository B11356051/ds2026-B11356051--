#!/bin/sh
set -e
cp /home/kong/temp.yml /usr/local/kong/kong.yml
exec /docker-entrypoint.sh "$@"
