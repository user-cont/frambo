This directory contains a reference implementation of a bot.
It's as simple as possible so you can take a look at how to implement new bot.

The directory might be eventually removed once we have some real bots implemented.

Parts:

- [foobar/](foobar/) - python package with bot implementation
- [setup.py](setup.py) - setuptools script to install foobar package in image
- [tasks.sh](tasks.sh) - celery worker start script
- [producer.py](producer.py) - submits a task, this is for testing the bot
- [../Dockerfile.example](../Dockerfile.example) - to create image with example bot
- [../docker-compose.yml](../docker-compose.yml) - see `example-bot` service

To implement your bot, you need:
1. a python module similar to `foobar/` and `tasks.sh` script
2. run `make redis-start` to start redis
3. set $APP and $QUEUE (see `docker-compose.yaml`) and run `tasks.sh`
4. run `python3 producer.py`
5. if you see `Task accepted` and `Task xyz succeeded` proceed to next steps
6. create Dockerfile similar to `Dockerfile.example`
7. run your containerized bot similar to example-bot in `docker-compose.yaml`
