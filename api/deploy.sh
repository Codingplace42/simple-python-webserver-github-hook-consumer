#!/bin/bash

while getopts d: flag
do
    case "${flag}" in
        d) directory_=${OPTARG};;
    esac
done

LOCAL_HASH=$(git -C $directory_ rev-parse HEAD)
git -C $directory_ pull origin master
REMOTE_HASH=$(git -C $directory_ rev-parse origin/master)

if [[ $LOCAL_HASH == $REMOTE_HASH ]]
then
    echo "HASH EQUAL"
else
    echo "HASH NOT EQUAL"
    # OPTIONAL ACTIONS HERE
fi
