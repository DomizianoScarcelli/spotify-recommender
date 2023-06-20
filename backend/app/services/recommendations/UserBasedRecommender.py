from utils.sparkSessionUtils import create_spark_session
from pyspark.sql import DataFrame
from typing import List
from models.Song import Song


class UserBasedRecommender:
    def __init__(self) -> None:
        self.spark, self.sc = create_spark_session()

    def test(self) -> DataFrame:
        values = [(1, 2), (3, 4), (5, 6)]
        df = self.sc.createDataFrame(values, ["num1", "num2"])
        return df

    def json_to_df(self, data: List[Song]):
        return
