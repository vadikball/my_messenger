#!/bin/sh
docker build -t my_messenger:latest .

docker build -t my_messenger_test:latest -f Dockerfile.test .

docker compose -f docker-compose.test.yml up --exit-code-from test_app

TEST_CODE=$?

docker compose -f docker-compose.test.yml down -v

exit $TEST_CODE
