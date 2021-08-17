#!/bin/bash

cd /usr/local/spark/sbin
./start-master.sh # starting org.apache.spark.deploy.master.Master, logging to /usr/local/spark/logs/
ps -ef | grep java
ls -lAt /usr/local/spark/logs
cat /usr/local/spark/logs/* | grep "Starting Spark master at"
# Write the spark URL to remember (suppose: "spark://my-spark:7077")
cat /usr/local/spark/logs/* | grep port
# Use the URL of Master to start the Slave
./start-slave.sh spark://localhost:7077

while true; do sleep 1000; done
