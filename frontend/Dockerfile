FROM node:18 AS build
WORKDIR /app/frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build --prod

FROM nginx:stable
COPY --from=build /app/frontend/dist/frontend /usr/share/nginx/html
