FROM ubuntu:trusty
MAINTAINER Sander Evers <sander.evers@topicus.nl>

RUN apt-get -q update
RUN apt-get -qy install git python

# init ssh
RUN mkdir -p /root/.ssh
ADD known_hosts /root/.ssh/known_hosts

# Copy python files
ADD java_exports.py /java_exports.py
ADD webserver.py /webserver.py

# Expose ports.
#   - 8888: HTTP
EXPOSE 8888

# Add start script
ADD start.sh /start.sh
RUN chmod +x /start.sh

# docker run --name ekspor_backend -e GIT_SSH_KEY="$(cat id_ekspor)" sandr/ekspor
ENTRYPOINT /start.sh