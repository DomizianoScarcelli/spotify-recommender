import os
import json
from tqdm import tqdm, trange
import requests
import math
import ast
import pandas as pd
import glob

# TODO: this changes every hour, so build a funciton that fetches it
AUTH_TOKEN = "BQCcqo23ViHg5jKJJYLtroSXuntLkbyJal3unKeReP8agVUlICZHyzdpiuupZSY3Glo9Oeov6d-4GF3Lmu9wkKUeaFK5fzDKO9sE0KcJx1yDb-QI1bsk"
# TODO: change path in order to be relative
DATA_PATH = "/Users/dov/Desktop/spotify_million_playlist_dataset/data"
SAVE_PATH = "/Users/dov/Desktop/spotify_million_playlist_dataset/saved"


def get_track_audio_feature(track_id):
    """
    Gets the audio features of a single track
    """
    URL = f"https://api.spotify.com/v1/audio-features/{track_id}"
    header = {'Authorization': 'Bearer ' + AUTH_TOKEN}
    res = requests.get(URL, headers=header)
    return res.json()


def get_tracks_audio_feature(tracks_ids):
    """
    Gets the audio features of a multiple tracks
    """

    URL = f"https://api.spotify.com/v1/audio-features"
    header = {'Authorization': 'Bearer ' + AUTH_TOKEN}
    payload = {'ids': tracks_ids}
    res = requests.get(URL, headers=header, params=payload)
    return res.status_code, res.json()


def get_tracks_id(path, save_path):
    """
    Retrieves the tracks id from the jsons files that describe the playlists, and saves them in a file
    """
    result = set()
    file_count = sum(len(files)
                     for _, _, files in os.walk(path))  # Get the number of files
    with tqdm(total=file_count) as pbar:
        for root, _, files in os.walk(path):
            for file in files:
                pbar.update(1)
                with open(os.path.join(root, file), "r") as f:
                    content = json.load(f)
                for playlist in content["playlists"]:
                    for track in playlist["tracks"]:
                        track_uri = track["track_uri"].replace(
                            "spotify:track:", "")
                        result.add(track_uri)
    set_to_string = ",".join(result)
    with open(save_path, "w") as f:
        f.write(set_to_string)
    return result


def extract_N_groups(N=100):
    """
    Creates lists of N in order to group songs in batches, and saves them into a new file
    """
    with open(os.path.join(SAVE_PATH, "all_songs.csv"), "r") as songs:
        tracks_ids = songs.read()
    track_list = tracks_ids.split(",")
    num_tracks = len(track_list)
    steps = math.ceil(num_tracks / N)
    N_group_tracks = []
    for i in range(steps):
        N_group_tracks.append(track_list[N*i:N*(i+1)])
    with open(os.path.join(SAVE_PATH, "N_groups.txt"), "w") as f:
        f.write(str(N_group_tracks))
    return N_group_tracks


def batch_track_list_feature_extraction(N_group_tracks, group_range):
    """
    Given a certain group range, it calls the api for all these song groups in order to extract the audio features
    """
    N_group_tracks = [N_group_tracks[i] for i in group_range]
    result = dict()
    for index, track_group in enumerate(tqdm(N_group_tracks)):
        status_code, content = get_tracks_audio_feature(",".join(track_group))
        if status_code == 200:
            result[index] = content
        else:
            raise Exception(
                f"API call failed with status code: {status_code}, error: {content}")
    return result


def create_tracks_feature_json(step_size=1000):
    """
    It execte the batch_track_list_feature_extraction for all the extracted songs, in batches in order to have partial results in case of failures
    """

    def execute_step(group_range):
        try:
            print(f"I'm currently in step: {step} with range: {group_range}")
            FEATURE_PATH = os.path.join(
                SAVE_PATH, f"tracks_features_{group_range}.json")
            if os.path.exists(FEATURE_PATH):
                print(
                    f"Path {FEATURE_PATH} already existing, skipping to the next one")
                return

            result = batch_track_list_feature_extraction(
                N_group_tracks, group_range=group_range)
            with open(FEATURE_PATH, "w") as f:
                json.dump(result, f)
        except Exception as e:
            print(e)

    with open(os.path.join(SAVE_PATH, "N_groups.txt"), "r") as f:
        N_group_tracks = f.read()
        N_group_tracks = ast.literal_eval(N_group_tracks)

    N_STEPS = math.ceil(len(N_group_tracks) / step_size)
    for step in trange(N_STEPS):
        group_range = range(step * step_size, (step+1) * step_size)
        print(f"I'm currently in step: {step} with range: {group_range}")
        try:
            execute_step(group_range)
        except IndexError as indexError:
            group_range = range(step * step_size, len(N_group_tracks))
            execute_step(group_range)


def extract_only_audio_features(dir_path, saved_path):
    """
    For each file, it only extracts the audio_features list in order to be read into a pyspark dataframe.
    """
    for filename in tqdm(os.listdir(dir_path)):
        if filename.endswith('.json'):
            with open(os.path.join(dir_path, filename), 'r') as f:
                data = json.load(f)
                audio_features_list = []
                try:
                    i = 0
                    while data[str(i)]:
                        audio_features_list.extend(
                            data[str(i)]['audio_features'])
                        i += 1
                except:
                    pass
                with open(os.path.join(saved_path, filename[:-5]+'_new.json'), 'w') as new_file:
                    json.dump(audio_features_list, new_file, indent=4)


def test_same_number_of_songs(json_path, all_songs_path):
    """
    Test if the number of song in the all_track_features.json is equal to the number of unique songs in the playlists
    """
    all_tracks_features = pd.DataFrame()
    json_pattern = os.path.join(json_path, '*.json')
    file_list = glob.glob(json_pattern)

    dfs = []
    for file in tqdm(file_list, desc="Loading audio features"):
        with open(file) as f:
            json_data = pd.json_normalize(json.loads(f.read()))
        dfs.append(json_data)
    # or sort=True depending on your needs
    all_tracks_features = pd.concat(dfs, sort=False)

    with open(all_songs_path, "r") as f:
        all_songs = f.read().split(",")

    num_songs_in_features = len(all_tracks_features.index)
    num_all_songs = len(all_songs)
    return abs(num_songs_in_features - num_all_songs)


if __name__ == "__main__":
    dir_path = "../../audio_features/track_features/"
    # saved_path = "../../audio_features/pyspark_track_features/"
    saved_path = "../../audio_features/splitted_pyspark_track_features/"
    # extract_only_audio_features(dir_path, saved_path)
    json_path = saved_path
    all_songs_path = "../../audio_features/all_songs.csv"
    # print(test_same_number_of_songs(json_path, all_songs_path))
