#!/bin/bash

POD_NETWORK_CIDR="10.244.0.0/16"
HOSTNAME="k8s-master"
HOST_IP="192.168.219.44"

# kubeadm init
sudo kubeadm init \
  --pod-network-cidr=${POD_NETWORK_CIDR} \
  --control-plane-endpoint="${HOSTNAME}:6443" \
  --apiserver-cert-extra-sans=${HOST_IP},${HOSTNAME}

# kubectl configuration
mkdir -p $HOME/.kube
sudo cp -f /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
