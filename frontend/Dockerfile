FROM node:12

MAINTAINER <berserg2010@gmail.com>

ARG APP_PATH=/usr/src/todo

WORKDIR $APP_PATH
RUN chown -R 1000:1000 $APP_PATH

RUN deluser --remove-home node \
  && useradd --home-dir $APP_PATH --uid 1000 --user-group node
#  && useradd --no-create-home --system --uid 1000 --user-group node
USER node

ENV PATH=$APP_PATH/node_modules/.bin:$PATH

COPY --chown=1000:1000 package*.json ./

RUN npm install && npm cache clean --force

COPY --chown=1000:1000 nuxt.config.js ./
COPY --chown=1000:1000 ./client ./client

RUN npm run build

#ENV NUXT_HOST=0.0.0.0
#ENV NUXT_PORT=3000
#
#ENV HOST 0.0.0.0
#EXPOSE 3000
