FROM nginx
MAINTAINER Sander Evers <sander.evers@topicus.nl>

#RUN echo env BACKEND_PORT_8888_TCP_ADDR\; >> /etc/nginx/nginx.conf
#RUN echo env BACKEND_PORT_8888_TCP_PORT\; >> /etc/nginx/nginx.conf
ADD default.conf /etc/nginx/conf.d/default.conf

#ADD start.sh /start.sh
#RUN chmod +x /start.sh

ADD d3.min.js /usr/share/nginx/html/d3.min.js
ADD index.html /usr/share/nginx/html/index.html

# docker run --rm -P --link ekspor_backend:backend --name ekspor_frontend quay.io/topicusonderwijs/ekspor-frontend
# ENTRYPOINT /start.sh
