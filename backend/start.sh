#!/bin/bash

if [ ${GITHUB_SSH_KEY} ]; then

    echo "${GITHUB_SSH_KEY}" > /root/.ssh/id_rsa
    chmod 600 /root/.ssh/id_rsa

    eval "$(ssh-agent -s)"
    ssh-add /root/.ssh/id_rsa

    mkdir /repos
    cd /repos
    git clone git@github.com:topicusonderwijs/cobra.git --depth 1 || git -C cobra pull
    git clone git@github.com:topicusonderwijs/eduarte.git --depth 1 || git -C eduarte pull
    git clone git@github.com:topicusonderwijs/digdag.git --depth 1 || git -C digdag pull

    rm /root/.ssh/id_rsa

elif [ ${GITHUB_OAUTH} ]; then

    mkdir /repos
    cd /repos
    # NB writes the secret into .git/config files!
    git clone https://${GITHUB_OAUTH}:@github.com/topicusonderwijs/cobra.git --depth 1 || git -C cobra pull
    git clone https://${GITHUB_OAUTH}:@github.com/topicusonderwijs/eduarte.git --depth 1 || git -C eduarte pull
    git clone https://${GITHUB_OAUTH}:@github.com/topicusonderwijs/digdag.git --depth 1 || git -C digdag pull

else

    echo Either pass in an SSH key through \$GITHUB_SSH_KEY or an OAuth token through
    echo \$GITHUB_OAUTH.

fi

cd /
python webserver.py
