FROM python:3.7

MAINTAINER <berserg2010@gmail.com>

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/todo/backend

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

RUN useradd --no-create-home --system --uid 1000 --user-group node
USER node

COPY . .
