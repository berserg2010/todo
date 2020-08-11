FROM node:12

MAINTAINER <berserg2010@gmail.com>

ARG APP_PATH=/usr/src/todo
#ENV PATH=$APP_PATH/node_modules/.bin:$PATH

WORKDIR $APP_PATH

#RUN deluser --remove-home node \
#  && addgroup -S node -g 1000 \
#  && adduser -S -G node -u 1000 node
RUN deluser --remove-home node \
  && useradd --no-create-home --system --uid 1000 --user-group node

COPY --chown=1000:1000 package*.json ./

RUN npm ci && npm cache clean --force

##RUN npm install -SE nuxt @nuxtjs/axios js-cookie
##RUN npm install -DE eslint-plugin-nuxt node-sass sass-loader

#WORKDIR $APP_PATH/frontend

COPY --chown=1000:1000 nuxt.config.js ./
COPY --chown=1000:1000 ./client ./client

RUN npm run build

#ENV NUXT_HOST=0.0.0.0
#ENV NUXT_PORT=3000

#ENV HOST 0.0.0.0
#EXPOSE 3000
