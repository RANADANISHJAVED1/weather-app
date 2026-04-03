#!/bin/bash

echo "========== Kubernetes Permission Setup =========="

# Ensure directories exist
echo "[1] Checking directories..."
if [ ! -d "/home/ubuntu/.kube" ] || [ ! -d "/home/ubuntu/.minikube" ]; then
  echo "ERROR: Minikube is not initialized for ubuntu user."
  echo "Run: minikube start (as ubuntu) first."
  exit 1
fi

# Add jenkins to ubuntu group (for shared access)
echo "[2] Adding jenkins user to ubuntu group..."
sudo usermod -aG ubuntu jenkins

# Set secure permissions (group-based access)
echo "[3] Setting permissions on kube and minikube directories..."
sudo chown -R ubuntu:ubuntu /home/ubuntu/.kube /home/ubuntu/.minikube

sudo chmod -R 750 /home/ubuntu/.kube
sudo chmod -R 750 /home/ubuntu/.minikube

# Ensure config file is readable
sudo chmod 640 /home/ubuntu/.kube/config

# Fix Minikube internal files (important)
sudo chmod -R g+rx /home/ubuntu/.minikube

# Set environment for all users (optional but useful)
echo "[4] Setting global KUBECONFIG..."
echo 'export KUBECONFIG=/home/ubuntu/.kube/config' | sudo tee /etc/profile.d/kubeconfig.sh > /dev/null

# Apply group changes immediately for jenkins (no logout needed)
echo "[5] Applying group permissions..."
sudo -u jenkins bash -c "newgrp ubuntu <<EOF
echo 'Jenkins now has ubuntu group access'
EOF"

echo "========== DONE =========="
echo ""
echo "Next steps:"
echo "1. Run Minikube as ubuntu:"
echo "   minikube start"
echo ""
echo "2. Test as ubuntu:"
echo "   kubectl get nodes"
echo ""
echo "3. Test as jenkins:"
echo "   sudo su - jenkins"
echo "   kubectl get nodes"
echo ""
echo "==============================================="