#!/bin/sh
sudo apt-get update
sudo apt-get install python-numpy -y
sudo apt-get install python-matplotlib -y
sudo gsutil cp gs://kdeyev_europe_west1/cwp.tar.gz /usr/local/bin/
cd /usr/local/bin
sudo tar xvf cwp.tar.gz 