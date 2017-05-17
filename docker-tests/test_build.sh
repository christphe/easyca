#/usr/bin/env bash

cd .. && make all && cd -
cp -r ../dist ./

## creating demoCA and certificate
date +%s > dist/date # create changing file to bust ca cache
docker build . -f dockerfiles/Dockerfile.ca -t easyca/dockertest-ca
docker run --cidfile=.cid easyca/dockertest-ca
docker cp $(cat .cid):demoCA/certs/ ./dist/certs
docker cp $(cat .cid):demoCA/cacert.pem ./dist/cacert.pem
docker rm $(cat .cid)
rm .cid

## creating servers
docker-compose build

## creating client
docker build . -f dockerfiles/Dockerfile.cli -t easyca/dockertest-cli