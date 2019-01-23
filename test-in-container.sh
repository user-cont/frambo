#!/bin/bash

set -ex

TIMESTAMP="$(date +%F-%H-%M-%S)"

TEST_IMAGE_NAME="frambo-tests"
CONTAINER_NAME="frambo-tests-${TIMESTAMP}"

gc() {
  retval=$?
  echo "Stopping test container"
  docker stop "${CONTAINER_NAME}" || :
  echo "Stopping redis container"
  docker-compose stop redis || :
  echo "Removing test containers"
  docker rm redis frambo_test_1 || :
  echo "Removing docker network"
  docker network rm "${FRAMBO_NET}" || :
  exit $retval
}

trap gc EXIT SIGINT

echo "Starting redis"
docker-compose up -d redis

echo "Starting test suite"
# To connect to redis started by docker-compose we have to specify
FRAMBO_NET=$(docker network ls | grep frambo | awk '{ print $2 }')
# docker network and REDIS_SERVICE_HOST
docker run --rm \
           --network ${FRAMBO_NET} \
           -e REDIS_SERVICE_HOST=redis \
           --name="${CONTAINER_NAME}" \
           "${TEST_IMAGE_NAME}"

echo "Test suite passed \\o/"
