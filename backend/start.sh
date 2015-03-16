#!/bin/bash

echo "$GIT_SSH_KEY" > /root/.ssh/id_rsa
chmod 600 /root/.ssh/id_rsa

eval "$(ssh-agent -s)"
ssh-add /root/.ssh/id_rsa

mkdir /repos
cd /repos
git clone git@github.com:topicusonderwijs/cobra.git --depth 1 || git -C cobra pull
git clone git@github.com:topicusonderwijs/eduarte.git --depth 1 || git -C eduarte pull
git clone git@github.com:topicusonderwijs/digdag.git --depth 1 || git -C digdag pull

cd /
python webserver.py
