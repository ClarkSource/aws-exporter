FROM python:3-alpine

MAINTAINER "CloudOps ClarkSource <CloudOps@clark.de>"
LABEL maintainer="CloudOps@clark.de"

COPY . /setup
WORKDIR /setup

RUN \
  apk add --no-cache --upgrade git && \
  python3 setup.py install && \
  apk del git && \
  rm -rf /setup /var/cache/apk 

EXPOSE 8000/tcp
CMD ["aws-exporter"]
