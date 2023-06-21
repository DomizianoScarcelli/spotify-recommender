from utils.sparkSessionUtils import create_spark_session
from pyspark.sql import DataFrame
from pyspark.sql.types import FloatType, StructType, ArrayType, StructField, IntegerType
from typing import List, Callable
from models.Song import Song
from pyspark.ml.linalg import VectorUDT, SparseVector
import pyspark.sql.functions as F
from functools import reduce
import numpy as np
import pickle
import os
from models.PysparkSchemas import playlist_schema, playlist_schema_mapped


class BaseRecommender:
    def __init__(self) -> None:
        self.spark, self.sc = create_spark_session()
        self.RATING_VECTOR_LENGTH: int = 681_805
        self.SOGNS_INFO_DF_PATH = "./pyspark_data/songs_info_df"
        self.SONGS_EMBEDDINGS_PATH = "./pyspark_data/song_embeddings"
        self.URI_TO_ID_PATH = os.path.abspath("./track_uri_to_id.pickle")
        self.load_assets()
        self.create_uri_to_id()

    def json_to_song_df(self, songs: List[Song]):
        return

    def load_assets(self):
        self.songs_info_df: DataFrame = self.spark.read.json(
            self.SOGNS_INFO_DF_PATH)
        self.songs_embeddings: DataFrame = self.spark.read.json(
            self.SONGS_EMBEDDINGS_PATH)

    def create_uri_to_id(self):
        self.songs_info_df.show()
        self.track_uri_to_id = self.songs_info_df.select(
            'track_uri', 'pos').rdd.collectAsMap()

    def load_uri_to_id(self, path: str):
        with open(path, "r") as f:
            self.track_uri_to_id: dict = pickle.load(f)

    def map_track_df_to_pos(self) -> DataFrame:
        """
        Returns a DataFrames containing the playlists, but the tracks are represented as a binary sparse vector.
        """
        @F.udf(returnType=VectorUDT())
        def extract_vector(tracks):
            pos_list = set()

            def reduce_fn(pos_list, row):
                pos_list.add(self.track_uri_to_id.get(row.track_uri))
                return pos_list

            pos_list = reduce(reduce_fn, tracks, pos_list)

            return SparseVector(self.RATING_VECTOR_LENGTH, sorted(list(pos_list)), [1 for _ in pos_list])

        # Apply the mapping UDF on the "tracks" column of the slice_df dataframe
        mapped_df = self.songs.withColumn(
            'tracks', extract_vector(F.col('tracks'))).withColumnRenamed("tracks", "rating_vector")

        return mapped_df

    def jaccard_similarity(self, vector_1: SparseVector, vector_2: SparseVector) -> float:
        """
        Computes the Jaccard Similarity between two sparse binary vectors
        """
        # Convert SparseVectors to sets
        set1 = set(vector_1.indices)
        set2 = set(vector_2.indices)

        # Calculate the intersection and union of the sets
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        # Calculate the similarity
        similarity = intersection / union

        return similarity

    def create_similarity_df(self, input_vector: DataFrame) -> DataFrame:
        input_vector_cached = input_vector.cache()
        input_vector = input_vector.first()[0]

        @F.udf(returnType=FloatType())
        def compute_similarity(vector1):
            return self.jaccard_similarity(vector1, input_vector)

        result_df = self.mapped_songs.withColumn(
            "similarity", compute_similarity(self.mapped_songs.rating_vector))

        input_vector_cached.unpersist()

        return result_df

    def get_top_k_results(similarity_df: DataFrame, k: int = 20) -> DataFrame:
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

    def perform_recommendation(self, songs: DataFrame):
        self.songs: DataFrame = songs
        self.mapped_songs: DataFrame = self.map_track_df_to_pos(self)
        self.input_vector: SparseVector = SparseVector(
            self.RATING_VECTOR_LENGTH, [1, 2, 3], [1, 1, 1])  # TODO: change to be dynamic
        self.similarity_df: DataFrame = self.create_similarity_df(
            self.input_vector)
        self.top_k_results: DataFrame = self.get_top_k_results(
            self.similarity_df, k=100)
        self.accumulated_top_k_results: DataFrame = self.accumulate_top_k_results(
            self.top_k_results, self.input_vector)
        self.top_n_recommendations = self.get_top_n_values(
            self, self.accumulated_top_k_results)
