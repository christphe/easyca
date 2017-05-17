#/usr/bin/env bash

# pre clean
./test_clean.sh > /dev/null 2>&1

## building test environment
./test_build.sh > /dev/null 2>&1

## launching servers
docker-compose up -d  > /dev/null 2>&1

## launching client
echo -n "Testing direct https connection... "
docker run --rm --net="host" --add-host="server:127.0.0.1" easyca/dockertest-cli curl https://server:10443 --cacert cacert.pem --silent > /dev/null 2>&1 && echo "Success" || echo "Error"
echo -n "Testing proxy configuration... "
docker run --rm --net="host" --add-host="server:127.0.0.1" easyca/dockertest-cli curl http://server:8080 --silent > /dev/null 2>&1 && echo "Success" || echo "Error"

# clean up
./test_clean.sh > /dev/null 2>&1
