# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from celery import Celery
from os import getenv
from raven import Client
from raven.contrib.celery import register_signal, register_logger_signal


def configure_sentry(dsn=None):
    dsn = dsn or getenv("SENTRY_DSN")
    if not dsn:
        return

    client = Client(dsn)
    # register a custom filter to filter out duplicate logs
    register_logger_signal(client)
    # hook into the Celery error handler
    register_signal(client)


def celery_app(include=None):
    """
    Create Celery instance. Take broker/backend url from environment.
    :param include: List of modules a worker should import. Depends on how you run a worker.
    If the xyz in 'celery worker --app=xyz' (see hack/tasks.sh) is a module then
    you don't need to specify anything in 'include'. But if the xyz is a package then you need to
    specify all modules from the package here.
    """
    redis_host = getenv("REDIS_SERVICE_HOST", "redis")
    redis_port = getenv("REDIS_SERVICE_PORT", "6379")
    redis_db = getenv("REDIS_SERVICE_DB", "0")
    redis_url = "redis://{host}:{port}/{db}".format(
        host=redis_host, port=redis_port, db=redis_db
    )

    # http://docs.celeryproject.org/en/latest/reference/celery.html#celery.Celery
    return Celery(backend=redis_url, broker=redis_url, include=include)


app = celery_app()
configure_sentry()
