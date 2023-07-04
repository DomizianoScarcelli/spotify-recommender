import requests
import os


class SpotifyClient:
    def __init__(self):
        self.token = None
        self.client_id = "e3abc052e89c45dab6b6a4f64809a380"
        self.client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]

    def _get_token(self):
        URL = f"https://accounts.spotify.com/api/token"
        data = {
            "grant_type": 'client_credentials',
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(URL, data=data)
        token = response["access_token"]
        self.token = token
        print("Spotify token: ", self.token)
        return token

    def _header_token(self):
        if not self.token:
            self._get_token()  # TODO: Insert the logic to update the token once expired
        return {
            f"'Authorization': 'Bearer {self.token}'"
        }

    def get_art_url(self, album_uri: str) -> str:
        album_id = album_uri.split(":")[-1]
        URL = f"https://api.spotify.com/v1/albums/{album_id}"
        data = requests.get(URL, headers=self._header_token())
        return data
