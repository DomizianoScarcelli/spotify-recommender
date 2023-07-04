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
