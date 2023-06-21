from pyspark.ml.linalg import VectorUDT
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType, FloatType, LongType

song_schema = StructType([
    StructField("pos", IntegerType(), True),
    StructField("artist_name", StringType(), True),
    StructField("track_uri", StringType(), True),
    StructField("artist_uri", StringType(), True),
    StructField("track_name", StringType(), True),
    StructField("album_uri", StringType(), True),
    StructField("duration_ms", LongType(), True),
    StructField("album_name", StringType(), True)
])

playlist_schema = StructType([
    StructField("name", StringType(), True),
    StructField("collaborative", StringType(), True),
    StructField("pid", IntegerType(), True),
    StructField("modified_at", IntegerType(), True),
    StructField("num_tracks", IntegerType(), True),
    StructField("num_albums", IntegerType(), True),
    StructField("num_followers", IntegerType(), True),
    StructField("tracks", ArrayType(song_schema), True),
    StructField("num_edits", IntegerType(), True),
    StructField("duration_ms", IntegerType(), True),
    StructField("num_artists", IntegerType(), True),
])

playlist_schema_mapped = StructType([
    StructField("name", StringType(), True),
    StructField("collaborative", StringType(), True),
    StructField("pid", IntegerType(), True),
    StructField("modified_at", IntegerType(), True),
    StructField("num_tracks", IntegerType(), True),
    StructField("num_albums", IntegerType(), True),
    StructField("num_followers", IntegerType(), True),
    StructField("tracks", VectorUDT(), True),
    StructField("num_edits", IntegerType(), True),
    StructField("duration_ms", IntegerType(), True),
    StructField("num_artists", IntegerType(), True),
])

audio_features_schema = StructType([
    StructField("danceability", FloatType(), True),
    StructField("energy", FloatType(), True),
    StructField("key", IntegerType(), True),
    StructField("loudness", FloatType(), True),
    StructField("mode", IntegerType(), True),
    StructField("speechiness", FloatType(), True),
    StructField("acousticness", FloatType(), True),
    StructField("instrumentalness", FloatType(), True),
    StructField("liveness", FloatType(), True),
    StructField("valence", FloatType(), True),
    StructField("tempo", FloatType(), True),
    StructField("type", StringType(), True),
    StructField("id", StringType(), True),
    StructField("uri", StringType(), True),
    StructField("track_href", StringType(), True),
    StructField("analysis_url", StringType(), True),
    StructField("duration_ms", LongType(), True),
    StructField("time_signature", IntegerType(), True)
])
