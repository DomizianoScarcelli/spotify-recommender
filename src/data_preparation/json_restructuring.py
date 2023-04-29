import json
import os
from tqdm import tqdm
import zipfile

# Set the directory where your JSON files are located
dir_path = '../../data/'
saved_path = "new_jsons/"

def extract_playlist_data(dir_path, saved_path):
    # Loop through each file in the directory
    for filename in tqdm(os.listdir(dir_path)):
        if filename.endswith('.json'):
            with open(os.path.join(dir_path, filename), 'r') as f:
                # Load the JSON file into a dictionary
                data = json.load(f)
                # Extract the 'playlists' key from the dictionary
                playlists = data['playlists']
                # Write the 'playlists' key to a new JSON file
                with open(os.path.join(saved_path, filename[:-5]+'_new_2.json'), 'w') as new_file:
                    json.dump(playlists, new_file, indent=4)

# extract_playlist_data(dir_path, saved_path)

def create_zip_archive(folder_path, archive_path):
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(folder_path):
            for file in tqdm(files, total=1001):
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))

folder_path = "./new_jsons"
destination_path = "./pyspark_friendly_spotify_playlist_dataset_nomacos.zip"

create_zip_archive(folder_path, destination_path)
