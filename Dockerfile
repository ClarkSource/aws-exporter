FROM python:3-alpine

MAINTAINER "CloudOps ClarkSource"
LABEL maintainer="CloudOps@clark.de"

COPY . /setup
WORKDIR /setup

RUN apk add git py3-setuptools --no-cache
RUN python3 setup.py install && rm -rf /setup

EXPOSE 8000/tcp
CMD ["aws-exporter"]

