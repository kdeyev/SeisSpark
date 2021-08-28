#!/bin/bash

cd /opt/bitnami/spark/sbin
./start-master.sh
./start-slave.sh spark://localhost:7077

while true; do sleep 1000; done
