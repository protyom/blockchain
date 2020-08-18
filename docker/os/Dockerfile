FROM python:3.7.9-buster

LABEL maintainer="protyom"

RUN apt-get update && \
    apt-get install apt-utils \
    openssl \
    libgdal-dev \
    libgeos++-dev \
    libproj-dev \
    libprotobuf-c-dev \
    g++ \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    musl-dev \
    libffi-dev \
    libghc-persistent-postgresql-dev \
    gettext \
    libxslt-dev -y

RUN pip3 install --upgrade pip
RUN pip3 install uwsgi