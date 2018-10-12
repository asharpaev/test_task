FROM python:2.7-alpine3.8

RUN pip install docker

COPY ./rootfs /

WORKDIR /app

ENTRYPOINT python main.py