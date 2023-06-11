from minio import Minio

ACCESS_KEY = "1eutzGk6yoc3Hf2dOAJ7"
SECRET_KEY = "d3dCXw9Zxj03mkYDKlZjQEv1zelIMUzD2i3t1t0W"


class MinioClient:
    def __init__(self):
        self.client = Minio(
            endpoint="http://localhost:9002",
            access_key=ACCESS_KEY,
            secret_key=SECRET_KEY
        )

    def dump_image(self, art_url: str):
        pass

    def get_image(self, song_uri: str):
        pass
