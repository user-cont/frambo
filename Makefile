.PHONY: redis-start redis-stop example-bot-build example-bot-start example-bot-stop example-bot-run-task test-build test-in-container image-build image-push clean

IMAGE_NAME = docker.io/usercont/frambo
TEST_IMAGE_NAME = frambo-tests

redis-start:
	docker-compose up redis flower redis-commander

redis-stop:
	docker-compose stop redis flower redis-commander

example-bot-build:
	docker-compose build example-bot

example-bot-start: example-bot-stop
	docker-compose up

example-bot-stop:
	docker-compose stop

example-bot-run-task:
	docker-compose exec example-bot python3 /tmp/example-bot/producer.py

test-build: image-build
	docker build --tag ${TEST_IMAGE_NAME} -f Dockerfile.tests .

test-in-container: test-build
	./test-in-container.sh

image-build:
	docker build --tag ${IMAGE_NAME} .

validate-bot-cfg: image-build
	docker run -it -v ${BOT_CFG_PATH}:/tmp/bot-cfg.yml:ro,Z \
	${IMAGE_NAME} bash -c "DEPLOYMENT=dev python3 /tmp/frambo/frambo/config.py /tmp/bot-cfg.yml"

image-push: image-build
	docker push ${IMAGE_NAME}

clean:
	find . -name '*.pyc' -delete
