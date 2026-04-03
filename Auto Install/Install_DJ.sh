#!/bin/bash

sudo apt update

echo "installing java"
sudo apt install fontconfig openjdk-21-jre -y
java -version

echo "installing jenkins"
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update -y
sudo apt install jenkins -y

echo "installing Docker"
sudo apt install docker.io -y
sudo usermod -aG docker ubuntu
sudo newgrp docker