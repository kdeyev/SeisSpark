#!/bin/bash

cd /opt/bitnami/spark/sbin
./start-master.sh
./start-slave.sh spark://localhost:7077

cd $SEISSPARK_HOME
python src/seisspark_service/main.py 
