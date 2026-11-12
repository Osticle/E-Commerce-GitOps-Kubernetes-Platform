#!/bin/bash

# You can change the version here
HELM_VERSION="v4.2.4"

wget https://get.helm.sh/helm-${HELM_VERSION}-linux-amd64.tar.gz
tar -zxvf helm-${HELM_VERSION}-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/helm

# Clean file
rm -rf helm-${HELM_VERSION}-linux-amd64.tar.gz linux-amd64

echo ""
echo 'Finished, please verify that helm is installed by running "helm"'