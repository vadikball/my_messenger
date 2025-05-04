#!/bin/sh
docker build -t my_messenger:latest .

docker build -t my_messenger_test:latest -f Dockerfile.test .

docker build -t my_messenger_dev:latest -f Dockerfile.dev .

docker compose -f docker-compose.dev.yml up
