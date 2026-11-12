#!/bin/bash

sudo apt install -y python3
sudo apt install -y python3-pip python3-ruamel.yaml

# Verify
echo "" && echo "INSTALLED SUCCESSFULLY"
python3 –-version
sudo -u python3 -c "import ruamel.yaml; print('ruamel.yaml is ready')"
