# Development stage
FROM node:18-alpine AS development

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

EXPOSE 3000
CMD ["npm", "start"]

# Build stage
FROM node:18-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM nginx:stable-alpine AS production

RUN rm -rf /usr/share/nginx/html/*
COPY --from=build /app/build /usr/share/nginx/html/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]