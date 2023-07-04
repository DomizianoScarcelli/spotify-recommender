from clients.MinioClient import MinioClient
from clients.LastfmClient import LastfmClient, ImageNotFoundError
from repository.SongsRepository import SongRepository
from tqdm import tqdm
import json
import os

minio_client = MinioClient()
lastfm_client = LastfmClient()
song_repository = SongRepository()


all_songs = song_repository.get_all_songs(
    paginated=False)  # Remove pagination or iterate over it

all_albums = {song["album_uri"]: (
    song["artist"], song["album"]) for song in all_songs}
objects_in_bucket = set(minio_client.get_object_names())

albums_not_found = set({0})
ALBUM_NOT_FOUND_PATH = "./album-not-found.pickle"

if os.path.exists(ALBUM_NOT_FOUND_PATH):
    with open(ALBUM_NOT_FOUND_PATH, "r") as f:
        albums_not_found = set(json.load(f))

albums_count = {}
for song in all_songs:
    album_uri = song["album_uri"]
    if album_uri not in albums_count:
        albums_count[album_uri] = 1
    else:
        albums_count[album_uri] += 1

print(
    f"There are {len(albums_count)} albums in album_count, {len([key for key, value in albums_count.items() if value > 1])} appear more than once!")


MIN_ALBUM_COUNT = 3

albums_to_add = {
    key: value for key, value in all_albums.items() if
    key not in objects_in_bucket and
    key not in albums_not_found and
    albums_count[key] >= MIN_ALBUM_COUNT
}

for index, (album_uri, (artist, album)) in enumerate(tqdm(albums_to_add.items())):
    try:
        image = lastfm_client.get_album_art(artist, album)
        minio_client.dump_image(image, album_uri)
    except ImageNotFoundError as e:
        albums_not_found.add(album_uri)
        if index % 100 == 0:
            with open(ALBUM_NOT_FOUND_PATH, "w") as f:
                json.dump(str(albums_not_found), f)
        print(
            f"Image wasn't found for the album: {album}, skipping...")
    except KeyboardInterrupt:
        raise KeyboardInterrupt()
    except:
        print("Other error found, skipping!")
