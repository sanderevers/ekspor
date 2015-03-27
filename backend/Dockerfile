FROM ubuntu:trusty
MAINTAINER Sander Evers <sander.evers@topicus.nl>

RUN apt-get -q update
RUN apt-get -qy install git python

# init ssh
RUN mkdir -p /root/.ssh
ADD ssh_config /root/.ssh/config

# Copy python files
ADD java_exports.py /java_exports.py
ADD webserver.py /webserver.py

# Expose ports.
#   - 8888: HTTP
EXPOSE 8888

# Add start script
ADD start.sh /start.sh
RUN chmod +x /start.sh

# docker run --name ekspor_backend -e GITHUB_SSH_KEY="$(cat id_ekspor)" sandr/backend
# docker run --name ekspor_backend -e GITHUB_OAUTH="$(cat github_oauth)" sandr/backend
ENTRYPOINT /start.sh
