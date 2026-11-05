##### Dockerfile #####
## build stage ##
FROM node:20-slim AS build

WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile --network-timeout 600000 && yarn cache clean

COPY . .
ENV GENERATE_SOURCEMAP=false
RUN yarn build

## run stage ##
FROM nginx:alpine
RUN mkdir /run
COPY --from=build /app/build /run
COPY nginx.conf /etc/nginx/nginx.conf