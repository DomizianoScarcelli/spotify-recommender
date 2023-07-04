from pyspark.ml.linalg import SparseVector
from typing import List


def jaccard_similarity(vector_1: SparseVector, vector_2: SparseVector) -> float:
    """
    Computes the Jaccard Similarity between two sparse binary vectors
    """

    set1 = set(vector_1.indices)
    set2 = set(vector_2.indices)

    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))

    similarity = intersection / union

    return similarity
