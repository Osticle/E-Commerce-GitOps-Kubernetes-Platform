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

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]