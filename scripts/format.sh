#!/bin/sh
autoflake --remove-unused-variables --remove-duplicate-keys --ignore-init-module-imports --remove-all-unused-imports -i -r app tests
black app tests
isort --profile black app tests
mypy app tests
flake8 app tests
