import requests
import os
import dotenv
import base64

dotenv.load_dotenv()


class ImageNotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class LastfmClient:
    def __init__(self):
        self.api = os.environ["LASTFM_API"]

    def get_album_art(self, artist_name: str, album_name: str):
        URL = 'http://ws.audioscrobbler.com/2.0/'
        params = {
            'method': 'album.getInfo',
            'api_key': self.api,
            'artist': artist_name,
            'album': album_name,
            "format": "json"
        }
        response = requests.get(URL, params=params).json()
        if "album" not in response:
            raise ImageNotFoundError(
                f"Image was not found for album: {album_name}")
        image_url = response["album"]["image"][1]["#text"]
        if image_url == "":
            raise ImageNotFoundError(
                f"Image was not found for album: {album_name}")
        image = requests.get(image_url).content
        encoded_image = base64.b64encode(image)
        return encoded_image
