#/usr/bin/env bash

# pre clean
./test_clean.sh > /dev/null 2>&1

## building test environment
./test_build.sh > /dev/null 2>&1

## launching server
docker run --rm --name easyca-server -p10443:443 -p10080:80 -d easyca/dockertest-server > /dev/null 2>&1

## launching client
docker run --rm --net="host" --add-host="server:127.0.0.1" easyca/dockertest-cli curl https://server:10443 --cacert cacert.pem --silent > /dev/null 2>&1 && echo "Success" || echo "Error"

# clean up
# ./test_clean.sh > /dev/null 2>&1
