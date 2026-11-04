##### Dockerfile #####
## build stage ##
FROM node:18.18-alpine AS build

WORKDIR /app
COPY ./package* .
RUN yarn install

COPY . .
RUN yarn build

## run stage ##
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]