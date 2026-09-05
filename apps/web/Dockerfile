FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
COPY apps/web/package.json ./apps/web/package.json
RUN npm ci
COPY apps/web ./apps/web
ARG VITE_API_URL=""
ARG VITE_DEMO_MODE="true"
ENV VITE_API_URL=$VITE_API_URL VITE_DEMO_MODE=$VITE_DEMO_MODE
RUN npm run build --workspace @kids/web

FROM nginx:1.27-alpine
COPY apps/web/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/apps/web/dist /usr/share/nginx/html
EXPOSE 80
