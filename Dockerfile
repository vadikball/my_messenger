FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1
ENV UVICORN_CMD_ARGS=""
ENV APP_PORT="8000"

EXPOSE ${APP_PORT}


# Create user for app
ENV APP_USER=appuser
RUN adduser -D -h /home/$APP_USER $APP_USER
WORKDIR /home/$APP_USER
USER $APP_USER

# Use venv directly via PATH
ENV VENV_PATH=/home/$APP_USER/.venv/bin
ENV USER_PATH=/home/$APP_USER/.local/bin
ENV PATH="$VENV_PATH:$USER_PATH:$PATH"

RUN pip install --user --no-cache-dir poetry && \
  poetry config virtualenvs.in-project true

COPY poetry.lock pyproject.toml README.md ./

COPY alembic.ini .
COPY app app
COPY tests tests

RUN poetry install --without dev

COPY scripts scripts

CMD sh "scripts/start.sh"
