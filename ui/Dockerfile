FROM node:lts-alpine as lint
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run lint

FROM node:lts-alpine as build
WORKDIR /app
COPY --from=lint /app ./
RUN npm run build

FROM node:lts-alpine as serve
WORKDIR /app/dist
RUN npm install -g http-server
COPY --from=build /app/dist ./
CMD [ "http-server", "."]