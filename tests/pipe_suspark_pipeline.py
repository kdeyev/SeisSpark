import pyspark
from pyspark.sql import SparkSession

from su_rdd.kv_operations import gather_from_rdd_key_value
from suspark.suspark_modules_factory import ModulesFactory, register_module_types
from suspark.suspark_pipeline import Pipeline

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

factory = ModulesFactory()
register_module_types(factory)


pipeline = Pipeline(spark_ctxt, factory)
suimp2d_id = pipeline.add_module("SUimp2d")
susort_id = pipeline.add_module("SUsort")
sufilter_id = pipeline.add_module("SUfilter")

gather_count_to_produce = 10
trace_count_per_gather = 5

with pipeline.get_module_w(suimp2d_id) as suimp2d:
    suimp2d.set_json_parameters({"nshot": gather_count_to_produce, "nrec": trace_count_per_gather})

with pipeline.get_module_r(sufilter_id) as sufilter:
    first_gather = gather_from_rdd_key_value(sufilter.rdd.first())

assert len(first_gather.traces) == trace_count_per_gather
print(first_gather.traces[0].buffer)
