#!/bin/sh
alembic upgrade head

fastapi run app/main.py --port $APP_PORT $UVICORN_CMD_ARGS & sleep 3 && pytest -vv tests
