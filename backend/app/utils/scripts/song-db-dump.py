# import requests
# import json


# def get_all_songs_w_info(playlist_df: DataFrame) -> DataFrame:
#     """
#     Given a playlist dataframe, returns the dataframe containing the unique list of songs with their relative info withing the entire playlist dataset.
#     """
#     all_songs = playlist_df.select(F.explode("tracks")).select(
#         'col.*').drop("pos").distinct()
#     return all_songs


# BASE_URL = "https://fb80-2001-b07-a5a-64c2-14bb-751b-ea04-fed6.ngrok-free.app"
# CREATE_SONG = f"{BASE_URL}/create-songs-batch"

# BATCH_SIZE = 5000
# for index in tqdm(range(0, len(all_songs_w_info), BATCH_SIZE)):
#     start_index = index + BATCH_SIZE
#     end_index = min(len(all_songs_w_info)-1, start_index + BATCH_SIZE)
#     songs = all_songs_w_info[start_index:end_index]
#     data = []
#     for i, row in enumerate(songs):
#         body = {
#             "id": start_index + i,
#             "name": str(row.track_name),
#             "artist": str(row.artist_name),
#             "album": str(row.album_name),
#             "duration": int(row.duration_ms),
#             "song_uri": row.track_uri,
#             "album_uri": row.album_uri
#         }
#         data.append(body)
#     requests.post(CREATE_SONG, json=data)
