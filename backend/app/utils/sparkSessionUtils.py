from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext
from typing import Tuple
from pyspark.sql import DataFrame


def create_spark_session() -> Tuple[SparkContext, SparkSession]:
    conf = SparkConf().\
        set('spark.ui.port', "4050").\
        set('spark.executor.memory', '12G').\
        set('spark.driver.memory', '12G').\
        set('spark.driver.maxResultSize', '100G').\
        setAppName("SparkSession").\
        setMaster("local[*]")
    try:
        sc = SparkContext(conf=conf)
    except:
        pass
    spark = SparkSession.builder.getOrCreate()
    return spark, sc
