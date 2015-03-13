#!/bin/bash

eval "$(ssh-agent -s)"
ssh-add /root/.ssh/id_rsa

cd /cobra
git pull
cd /eduarte
git pull
cd /digdag
git pull

cd /
python webserver.py
