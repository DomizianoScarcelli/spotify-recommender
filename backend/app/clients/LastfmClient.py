import requests
import dotenv
import os

dotenv.load_dotenv("../../.env")


class LastfmClient:
    def __init__(self):
        self.api = os.environ["LASTFM_API"]

    def get_album_art(self, artist_name: str, album_name: str):
        URL = 'http://ws.audioscrobbler.com/2.0/'
        params = {
            'method': 'album.getInfo',
            'api_key': self.api,
            'artist': artist_name,
            'album': album_name
        }
        response = requests.get(URL, params=params)
        image_url = response["album"]["image"][1]["#text"]
        image = requests.get(image_url)
        return image.raw
