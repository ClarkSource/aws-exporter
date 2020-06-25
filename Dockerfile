FROM python:3-alpine

MAINTAINER "CloudOps ClarkSource <CloudOps@clark.de>"
LABEL maintainer="CloudOps@clark.de"

RUN apk add --upgrade apk-tools --no-cache && apk upgrade --available --no-cache && apk add git py3-setuptools --no-cache

COPY . /setup
WORKDIR /setup
RUN python3 setup.py install && rm -rf /setup

EXPOSE 8000/tcp
CMD ["aws-exporter"]

