# Frambo

Framework for our automation bots.

## Vision of this project

Originally we started working on bots without any central infrastructure. We
reached a point where we realized that the software does not scale and it's
hard to maintain. Therefore this project should be focused on following
capabilities:

* Security hardening
  * don't run as root in the container
  * don't store passwords in the containers
  * dedicated identity for bots
* Use ansible/makefiles for automation
* Automate build & release & deploy process
* 100% automated
  * ideally via dist-git & osbs (eat own dog food)
* images are stored in a registry
* Validation is in-place
* staging environment
* Monitoring
  * seamless monitoring - when something goes wrong, we are first to know that and we know relevant info to resolve the issue ASAP
  * metrics - have a dashboard where we can see statistics
* Container entrypoint scripts
  * ideally have no entrypoints scripts and keep all the logic in bots

## Repository content

### frambo

Proof of concept of using [Celery](http://www.celeryproject.org) (asynchronous task queue based on distributed message passing) to organize bots.

There's a [docker-compose.yml](docker-compose.yml) to test it locally or [scripts](openshift) to deploy to OpenShift.

It's configured to use [Redis](https://redis.io) as
[broker](http://docs.celeryproject.org/en/latest/getting-started/brokers/redis.html) and
[backend](http://docs.celeryproject.org/en/latest/userguide/configuration.html#conf-redis-result-backend)

#### How to use pagure module in your bots

Frambo provides couple variables from  [pagure.py](./frambo/pagure.py):
* PAGURE_HOST ... which refers to `pagure.io` in case of `DEPLOYMENT=prod` or `stg.pagure.io` for other DEPLOYMENT values.
This variable is mainly used for clonning repositories and execution `git` operations.
* PAGURE_URL ... refers to `https://{PAGURE_HOST}/`

In your bot, you can e.g. ask for username by code:
```python
import requests

from frambo.fedora_pagure import PAGURE_URL

url = f"{PAGURE_URL}/api/0/-/whoami"
r = requests.post(url, headers={'Authorization': 'token {}'.format(pagure_api_token)})

```

where `pagure_api_token` taken from [token page](https://pagure.io/settings#nav-api-tab)

#### How to test/play with it ?

To test it locally start our example bot with `make example-bot-start`.
Run `make example-bot-build` before first run, `example-bot-start` doesn't depend on it to not rebuild with each tiny change.
It starts one celery worker, listening on queue defined in [docker-compose.yml](docker-compose.yml).
In other terminal verify that it works correctly by running `make example-bot-run-task`, which sends one task to the queue.

There's also [Flower](http://flower.readthedocs.io) (monitoring tool), which runs on [http://localhost:5555](http://localhost:5555/).
After running `make example-bot-run-task` you should see [one succeeded task there](http://localhost:5555/tasks?state=SUCCESS).

To check content of the redis instance there's redis-commander running on [http://localhost:8081](http://localhost:8081).

#### How to implement new bot ?

See [examples/bot/](./examples/bot/) directory for example bot implementation.
If you have any questions don't hesitate to ask and we'll update the documentation with answers.
