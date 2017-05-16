#/usr/bin/env bash

# clean mess
rm -rf dist

## stop server
docker stop easyca-server > /dev/null 2>&1 