# =============================================================================
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
# =============================================================================
import os
from zipfile import ZipFile

import pyspark
from pyspark.sql import SparkSession


def zipdir(path: str, ziph: ZipFile) -> None:
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, "..")))


class SeisSparkContext:
    def __init__(self) -> None:
        seisspark_home = os.environ["SEISSPARK_HOME"]
        seisspark_zip_pile = "seisspark.zip"

        if os.path.exists(seisspark_zip_pile):
            os.remove(seisspark_zip_pile)

        with ZipFile(seisspark_zip_pile, mode="a") as myzipfile:
            zipdir(f"{seisspark_home}/src/su_data", myzipfile)
            zipdir(f"{seisspark_home}/src/su_rdd", myzipfile)
            zipdir(f"{seisspark_home}/src/seisspark", myzipfile)
            zipdir(f"{seisspark_home}/src/seisspark_modules", myzipfile)

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
        spark_ctxt.addPyFile(seisspark_zip_pile)

        self._spark_ctxt = spark_ctxt

    @property
    def context(self) -> pyspark.SparkContext:
        return self._spark_ctxt
