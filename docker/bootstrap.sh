#!/bin/bash
#=============================================================================
# Copyright (c) 2021 SeisSpark (https://github.com/kdeyev/SeisSpark).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#=============================================================================

cd /opt/bitnami/spark/sbin
./start-master.sh # starting org.apache.spark.deploy.master.Master, logging to /usr/local/spark/logs/
ps -ef | grep java
ls -lAt /usr/local/spark/logs
cat /usr/local/spark/logs/* | grep "Starting Spark master at"
# Write the spark URL to remember (suppose: "spark://my-spark:7077")
cat /usr/local/spark/logs/* | grep port
# Use the URL of Master to start the Slave
./start-slave.sh spark://localhost:7077

while true; do sleep 1000; done
