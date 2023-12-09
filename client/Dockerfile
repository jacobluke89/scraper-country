FROM node:18-alpine  as build-deps

WORKDIR /usr/src/app

ARG REACT_APP_COUNTRY_DATA_VISUALISER_BASE_URL
ENV REACT_APP_COUNTRY_DATA_VISUALISER_BASE_URL $REACT_APP_COUNTRY_DATA_VISUALISER_BASE_URL

COPY package*.json ./

RUN npm ci --legacy-peer-deps

COPY ./src ./src
COPY .tsconfig.json ./tsconfig.json
COPY ./public ./public

RUN npm run build build

EXPOSE 3000

CMD [ "npm", "start" ]