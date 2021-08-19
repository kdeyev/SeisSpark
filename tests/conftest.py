import pyspark
import pytest
from pyspark.sql import SparkSession

from suspark.suspark_modules_factory import ModulesFactory, register_module_types


@pytest.fixture(scope="session")
def spark_ctxt() -> pyspark.SparkContext:

    spark_conf = pyspark.SparkConf()
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
    spark_reader = spark_sess.read
    spark_streamReader = spark_sess.readStream
    spark_ctxt.setLogLevel("WARN")
    return spark_ctxt


@pytest.fixture()
def modules_factory() -> ModulesFactory:

    factory = ModulesFactory()
    register_module_types(factory)
    return factory
