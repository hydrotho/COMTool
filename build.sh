#!/usr/bin/env bash

docker build -t comtool-complier .

docker run --rm \
    -e USER_ID=$UID \
    -e GROUP_ID=$GID \
    --mount type=bind,src=$PWD,dst=/code \
    comtool-complier
