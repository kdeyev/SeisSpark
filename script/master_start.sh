#!/bin/sh

gcsfuse kdeyev /mnt/gcs-bucket

export HADOOP_HOME=/usr/lib/hadoop
export CWPROOT=/usr/local/bin/cwp
export JAVA_HOME=/usr

cd ~/seismichadoop
./bin/suhdp load -input /mnt/gcs-bucket/7o_5m_final_vtap.segy -output poststack.sgy
./bin/suhdp load -input /mnt/gcs-bucket/prestack.segy -output prestack.sgy

cd ~/SeisSpark
#/usr/lib/spark/bin/pyspark_k enEngineUT.py
/usr/lib/spark/bin/pyspark_k SeisSparkWUI.py