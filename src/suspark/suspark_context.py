import os

import pyspark
from pyspark.sql import SparkSession


class SusparkContext:
    def __init__(self) -> None:

        spark_conf = pyspark.SparkConf()
        if "SPARK_MASTER_URL" in os.environ:
            spark_conf.setMaster(os.environ["SPARK_MASTER_URL"])
        # spark_conf.setAll([
        #     ('spark.master', ),
        #     ('spark.app.name', 'myApp'),
        #     ('spark.submit.deployMode', 'client'),
        #     ('spark.ui.showConsoleProgress', 'true'),
        #     ('spark.eventLog.enabled', 'false'),
        #     ('spark.logConf', 'false'),
        #     ('spark.driver.bindAddress', 'vps00'),
        #     ('spark.driver.host', 'vps00'),
        # ])

        spark_sess = SparkSession.builder.config(conf=spark_conf).getOrCreate()
        spark_ctxt = spark_sess.sparkContext
        spark_sess.read
        spark_sess.readStream
        spark_ctxt.setLogLevel("WARN")

        self._spark_ctxt = spark_ctxt

    @property
    def context(self) -> pyspark.SparkContext:
        return self._spark_ctxt
