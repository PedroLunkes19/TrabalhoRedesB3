FROM nginx:1.31.3-alpine-slim

COPY index.html /usr/share/nginx/html/index.html
COPY script.js /usr/share/nginx/html/script.js

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80