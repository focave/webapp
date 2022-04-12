# syntax=docker/dockerfile:1.3
FROM node:17

WORKDIR /frontend

RUN apt-get update
RUN apt-get install -y netcat

RUN chown -Rh node:node ./

USER node

COPY --chown=node:node . .

RUN mkdir ~/.npm-global && npm config set prefix '~/.npm-global'
ENV PATH="~/.npm-global/bin:${PATH}"

RUN npm install -g npm
RUN npm install