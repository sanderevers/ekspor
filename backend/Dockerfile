FROM ubuntu:trusty
MAINTAINER Sander Evers <sander.evers@topicus.nl>

RUN apt-get -q update
RUN apt-get -qy install git python

# copy ssh key
RUN mkdir -p /root/.ssh
ADD id_ekspor /root/.ssh/id_rsa
ADD known_hosts /root/.ssh/known_hosts

# get git repos
RUN eval "$(ssh-agent -s)" && \
    ssh-add /root/.ssh/id_rsa && \
    git clone git@github.com:topicusonderwijs/cobra.git && \
    git clone git@github.com:topicusonderwijs/eduarte.git && \
    git clone git@github.com:topicusonderwijs/digdag.git

# Copy python files
ADD java_exports.py /java_exports.py
ADD webserver.py /webserver.py

# Expose ports.
#   - 8888: HTTP
EXPOSE 8888

# Add start script
ADD start.sh /start.sh
RUN chmod +x /start.sh

# Start script
ENTRYPOINT /start.sh
