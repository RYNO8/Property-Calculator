# syntax=docker/dockerfile:1

# https://docs.docker.com/language/python/build-images/

# FROM python:3.8.0-slim
FROM python:3.8.10

WORKDIR /property-vis/src

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# code is "baked" into docker image
# comment out if not required to be "baked" in
# COPY . .

ENTRYPOINT [ "python3" ]
