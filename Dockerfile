FROM python:3-alpine

LABEL maintainer="cloudops@clark.de"

COPY . /setup
#WORKDIR /setup

RUN \
  apk add --no-cache --upgrade git && \
  pip install ./setup && \
  rm -rf ./setup && \
  apk del git && \
  rm -rf /setup /var/cache/apk 

EXPOSE 8000/tcp
CMD ["aws-exporter"]
