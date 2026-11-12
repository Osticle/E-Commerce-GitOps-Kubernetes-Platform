#!/bin/bash

GITLAB_DISTRIBUTION="gitlab-ce"

sudo apt update
curl --location "https://packages.gitlab.com/install/repositories/gitlab/${GITLAB_DISTRIBUTION}/script.deb.sh" | sudo bash
sudo apt install ${GITLAB_DISTRIBUTION}
