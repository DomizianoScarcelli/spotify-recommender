from utils.sparkSessionUtils import create_spark_session
from pyspark.sql import DataFrame, Row
from pyspark.sql.types import FloatType, StructType, ArrayType, StructField, IntegerType
from typing import List, Callable
from models.Requests import SongRequest
from pyspark.ml.linalg import VectorUDT, SparseVector
import pyspark.sql.functions as F
import numpy as np
import pickle
import os
from models.PysparkSchemas import playlist_schema_mapped, song_request_schema
import json
from utils.similarity_functions import jaccard_similarity

spark, sc = create_spark_session()


class UserBasedRecommender:
    def __init__(self) -> None:
        self.RATING_VECTOR_LENGTH: int = 681_805
        self.SOGNS_INFO_DF_PATH = "./pyspark_data/songs_info_df"
        self.SONGS_EMBEDDINGS_PATH = "./pyspark_data/songs_embeddings"
        self.URI_TO_ID_PATH = os.path.abspath("./track_uri_to_id.pickle")
        self.load_assets()
        self.create_uri_to_id()

    def json_to_song_df(self, songs: List[SongRequest]) -> DataFrame:
        """
        Given a playlist representation as a List of Songs, it converts it into a pyspark Dataframe
        """
        songs = [json.loads(song.json()) for song in songs]
        rdd = spark.sparkContext.parallelize(songs)
        df = spark.read.schema(song_request_schema).json(rdd)
        df.show()
        return df

    def sparse_vector_encoding(self, songs: DataFrame) -> SparseVector:
        """
        Given a DataFrame that represents a playlist, it returns the SparseVector that encodes it
        """
        indices = set()
        row: Row
        for row in songs.collect():
            indices.add(self.track_uri_to_id.get(row.song_uri))
        return SparseVector(self.RATING_VECTOR_LENGTH, sorted(list(indices)), [1 for _ in indices])

    def load_assets(self):
        self.songs_info_df: DataFrame = spark.read.json(
            self.SOGNS_INFO_DF_PATH)
        self.songs_embeddings: DataFrame = spark.read.schema(playlist_schema_mapped).json(
            self.SONGS_EMBEDDINGS_PATH)
        self.songs_embeddings = self.songs_embeddings.withColumnRenamed(
            "tracks", "rating_vector")

    def create_uri_to_id(self):
        self.track_uri_to_id = self.songs_info_df.select(
            'track_uri', 'pos').rdd.collectAsMap()

    def load_uri_to_id(self, path: str):
        with open(path, "r") as f:
            self.track_uri_to_id: dict = pickle.load(f)

    def create_similarity_df(self, similarity_function: Callable) -> DataFrame:

        input_vector = SparseVector(
            self.input_vector.size, self.input_vector.indices, self.input_vector.values)

        @F.udf(returnType=FloatType())
        def compute_similarity(vector1: SparseVector):
            return similarity_function(vector1, input_vector)

        result_df = self.songs_embeddings.withColumn(
            "similarity", compute_similarity(F.col("rating_vector")))

        return result_df

    def get_top_k_results(self, similarity_df: DataFrame, k: int) -> DataFrame:
        return similarity_df.filter((F.col("similarity") > 0)).orderBy(F.col("similarity").desc()).limit(k)

    def accumulate_top_k_results(self, top_k_results: DataFrame, input_vector: np.ndarray) -> DataFrame:
        @F.udf(returnType=VectorUDT())
        def sum_vector(sparse_vectors, similarities):
            similarities = np.array(similarities)
            sparse_vectors = np.array(sparse_vectors)
            # Compute the sum(vector * similarity) for each vector and similarity
            acc = np.dot(sparse_vectors.T, similarities)
            acc /= similarities.sum()  # Normalize the vector
            # If a song is present in the input playlist, don't consider it
            acc -= (input_vector * acc)
            return SparseVector(acc.size, np.nonzero(acc)[0], acc[np.nonzero(acc)])

        return top_k_results.agg(sum_vector(F.collect_list('rating_vector'), F.collect_list("similarity")).alias('summed'))

    def get_top_n_values(self, accumulated_top_k_results):
        @F.udf(returnType=ArrayType(
            StructType([
                StructField("pos", IntegerType(), False),
                StructField("confidence", FloatType(), False)
            ])))
        def get_top_n_values_udf(vector: SparseVector, n: int = 10):
            sorted_elements = vector.toArray().tolist()
            top_n_indices = sorted(range(len(sorted_elements)),
                                   key=lambda i: sorted_elements[i], reverse=True)[:n]
            return [(index, sorted_elements[index]) for index in top_n_indices]
        return accumulated_top_k_results.withColumn("top_n_recommendations", get_top_n_values_udf(
            F.col("summed"))).select(F.explode("top_n_recommendations")).select("col.*")

    def recommendation_song_info(self, recommendation: DataFrame, songs_info_df: DataFrame) -> DataFrame:
        return recommendation.join(songs_info_df, "pos")

    def perform_recommendation(self, songs: List[SongRequest]) -> DataFrame:
        self.songs = self.json_to_song_df(songs)
        self.input_vector = self.sparse_vector_encoding(
            self.songs)

        self.similarity_df = self.create_similarity_df(
            similarity_function=jaccard_similarity)

        self.top_k_results = self.get_top_k_results(
            similarity_df=self.similarity_df, k=10)
        self.accumulated_top_k_results = self.accumulate_top_k_results(
            self.top_k_results, self.input_vector.toArray())

        self.top_n_recommendations = self.get_top_n_values(
            self.accumulated_top_k_results)

        self.recommendation_info = self.recommendation_song_info(
            self.top_n_recommendations, self.songs_info_df)

        final_reccomendations = self.recommendation_info.collect()

        # track_uri -> similarity
        return [{"track_uri": item[-1], "similarity": item[-2]} for item in final_reccomendations]
