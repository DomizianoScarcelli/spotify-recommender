import os
import json
from tqdm import tqdm, trange
import requests
import math
import ast

#TODO: this changes every hour, so build a funciton that fetches it
AUTH_TOKEN = "BQCcqo23ViHg5jKJJYLtroSXuntLkbyJal3unKeReP8agVUlICZHyzdpiuupZSY3Glo9Oeov6d-4GF3Lmu9wkKUeaFK5fzDKO9sE0KcJx1yDb-QI1bsk"
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
    file_count = sum(len(files) for _, _, files in os.walk(path))  # Get the number of files
    with tqdm(total=file_count) as pbar:
        for root, _, files in os.walk(path):
            for file in files:
                pbar.update(1)
                with open(os.path.join(root, file), "r") as f:
                    content = json.load(f)
                for playlist in content["playlists"]:
                    for track in playlist["tracks"]:
                        track_uri = track["track_uri"].replace("spotify:track:", "")
                        result.add(track_uri)
    set_to_string = ",".join(result)
    with open(save_path, "w") as f:
       f.write(set_to_string)
    return result

def extract_N_groups(N = 100):
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
            raise Exception(f"API call failed with status code: {status_code}, error: {content}")
    return result

def create_tracks_feature_json(step_size=1000):
    """
    It execte the batch_track_list_feature_extraction for all the extracted songs, in batches in order to have partial results in case of failures
    """

    def execute_step(group_range):
        try:
            print(f"I'm currently in step: {step} with range: {group_range}")
            FEATURE_PATH = os.path.join(SAVE_PATH, f"tracks_features_{group_range}.json")
            if os.path.exists(FEATURE_PATH):
                print(f"Path {FEATURE_PATH} already existing, skipping to the next one")
                return

            result = batch_track_list_feature_extraction(N_group_tracks, group_range=group_range)
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
           

def unify_tracks_features_files(path):
    """
    Unifies all the track_features.json into a single one
    """
    result = dict()
    for root, dirs, files in os.walk(path):
        for file in files:
            filename = os.path.join(root, file)
            with open(filename, "r") as f:
                content = json.load(f)
            for i in content:
                group = content[i]
                tracks_features = group["audio_features"]
                for feature in tracks_features:
                    if feature is None:
                        continue
                    track_id = feature["id"]
                    if track_id not in result:
                        result[track_id] = feature
    with open(os.path.join(SAVE_PATH, "all_tracks_features.json"), "w") as f:
        json.dump(result, f)
    return result

def test_same_number_of_songs():
    """
    Test if the number of song in the all_track_features.json is equal to the number of unique songs in the playlists
    """
    with open(os.path.join(SAVE_PATH, "all_tracks_features.json"), "r") as f:
        result = json.load(f)
    with open(os.path.join(SAVE_PATH, "all_songs.csv"), "r") as f:
        all_songs = f.read().split(",")
    num_songs_in_features = len(result.keys())
    num_all_songs = len(all_songs)
    return abs(num_songs_in_features - num_all_songs)

if __name__ == "__main__":
    pass