FROM nginx:1.19.0-alpine

# configure supervisor
RUN apk add supervisor
RUN mkdir /run/daphne/
RUN rm /etc/supervisord.conf
COPY supervisord.conf /etc/supervisord.conf

# configure nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
