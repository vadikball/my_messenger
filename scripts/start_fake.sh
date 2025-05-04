#!/bin/sh
alembic upgrade head

poetry run populate

fastapi run app/main.py --port $APP_PORT $UVICORN_CMD_ARGS
