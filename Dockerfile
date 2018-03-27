FROM python:3.6-alpine

RUN apk add --no-cache --virtual .build-deps \
      build-base \
      libffi-dev \
      mariadb-dev && \
    apk add --no-cache --virtual .runtime-deps \
      mariadb-client-libs

ENV PYTHONUNBUFFERED 1

ENV LIBRARY_PATH=/lib:/usr/lib

RUN mkdir /code

WORKDIR /code

ADD ./requirements.txt /code/

RUN pip install -r requirements.txt && apk del .build-deps

ADD src/ /code/
