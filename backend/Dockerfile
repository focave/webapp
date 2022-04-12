# syntax=docker/dockerfile:1.3
FROM python:3.10
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install -y netcat


RUN useradd -m python
ENV PATH="/home/python/.local/bin:${PATH}"
USER python
WORKDIR /backend

COPY --chown=python:python requirements.txt .
RUN pip install -r requirements.txt


COPY --chown=python:python . .