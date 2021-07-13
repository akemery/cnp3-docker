#!/bin/bash

mv ssh .ssh
chmod 600 .ssh/id_rsa
eval "$(ssh-agent -s)"
ssh-add .ssh/id_rsa
mkdir ~/.ssh
ssh-keyscan github.com >> ~/.ssh/known_hosts