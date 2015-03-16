#!/bin/bash

# substitute fake variable $backend
sed -e "s/\$backend/$BACKEND_PORT_8888_TCP_ADDR:$BACKEND_PORT_8888_TCP_PORT/" -i "" /etc/nginx/conf.d/default.conf
nginx -g "daemon off;"
