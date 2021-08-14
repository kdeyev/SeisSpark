"""
   Copyright 2016 Kostya Deyev

   Licensed under the Apache License, Version 2.0 (the License);
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       httpwww.apache.orglicensesLICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an AS IS BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from pyspark import SparkContext, SparkConf
import seisspark

#######
# Spark
#######
conf = SparkConf().setAppName("appName").setMaster("local")
sc = SparkContext(conf=conf)

#####
# filenames
####
filenameSGY = '7o_5m_final_vtap.segy'
filenameRDD = 'poststack.sgy'  # "prestack.sgy"

#data = [1, 2, 3, 4, 5]
#distData = sc.parallelize(data)
#distData = distData.map(lambda x: (None, x))
# distData.saveAsSequenceFile("/test.txt")
#exit ()

#######
# SGY tests
#######
#testDrawSGY (filename)
#testPipe (filename, '/home/cloudera/SeisSpark/cwp/bin/sufilter', 'f=10,20,40,50')

#######
# HDFS
#######
#exportSGY ("prestack.sgy", 'ttt.sgy')
#importSGY ('7o_5m_final_vtap.segy', 'test9.sgy')
#drawSGY ('7o_5m_final_vtap.segy')


rdd = seisspark.loadData(sc, filenameRDD)
seisspark.drawRDD(rdd, 'initial rdd')

rdd = seisspark.Processing(
    ['/home/cloudera/SeisSpark/cwp/bin/sufilter', 'f=10,20,40,50']).do(rdd)

seisspark.drawRDD(rdd, 'after BP')

rdd = seisspark.SetKeyByHeader('cdp').do(rdd)

rdd = seisspark.FilterByHeader('cdp', 3001, 3200).do(rdd)
rdd = rdd.sortByKey()

# TODO GroupByHeader doesnt work correctly
rdd = seisspark.GroupByHeader('FieldRecord').do(rdd)
rdd = rdd.sortByKey()

seisspark.saveData(rdd, 'out1.sgy')


# spark-submit my_script.py
#./suhdp load -input ~/7o_5m_final_vtap.segy -output sss.sgy
# hdfs dfs -ls
# PYSPARK_PYTHON=/opt/cloudera/parcels/Anaconda/bin/python
