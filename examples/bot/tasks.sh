#!/usr/bin/bash

# Bots startup script
# $APP defines where's the bot's module (or package)
# $WORKER_QUEUES defines what queue(s) does a worker listen on

if [[ -z ${APP} ]]; then
    echo "APP not defined or empty, exiting"
    exit 1
fi

if [[ -z ${WORKER_QUEUES} ]]; then
    echo "WORKER_QUEUES not defined or empty, exiting"
    exit 1
fi

echo "Queues: ${WORKER_QUEUES}"

exec celery worker --app=${APP} --queues="${WORKER_QUEUES}" --loglevel=debug
