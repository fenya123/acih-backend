FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    # we need 'enchant-2' for pylint's spellchecker
    && apt-get -y install enchant-2 \
    && pip install --upgrade pip \
    && pip install poetry==1.5.1

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --with=app,test

COPY . ./
