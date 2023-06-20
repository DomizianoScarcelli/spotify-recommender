from clients.MinioClient import MinioClient
from clients.LastfmClient import LastfmClient, ImageNotFoundError
from repository.SongsRepository import SongRepository
from tqdm import tqdm

minio_client = MinioClient()
lastfm_client = LastfmClient()
song_repository = SongRepository()


all_songs = song_repository.get_all_songs(
    paginated=False)  # Remove pagination or iterate over it
objects_in_bucket = minio_client.get_object_names()

for song in tqdm(all_songs):
    if song["album_uri"] in objects_in_bucket:
        continue
    try:
        image = lastfm_client.get_album_art(song["artist"], song["album"])
        minio_client.dump_image(image, song["album_uri"])
    except ImageNotFoundError as e:
        print(
            f"Image wasn't found for the album: {song['album']}, skipping...")
    except:
        print("Another error occurred, skipping album...")
