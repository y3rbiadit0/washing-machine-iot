FROM python:3.11-slim-bookworm as runtime

RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app
COPY pyproject.toml poetry.lock README.md ./
RUN ["poetry", "install"]
RUN ["rm", "-rf", "$POETRY_CACHE_DIR"]

COPY . /app
RUN ["poetry", "install"]
EXPOSE 8000
ENTRYPOINT ["poetry", "run", "uvicorn", "main:app", "--proxy-headers", "--reload", "--host", "0.0.0.0", "--port", "8000"]