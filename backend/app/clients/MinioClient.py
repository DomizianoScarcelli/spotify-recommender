from minio import Minio
import io
ACCESS_KEY = "1eutzGk6yoc3Hf2dOAJ7"
SECRET_KEY = "d3dCXw9Zxj03mkYDKlZjQEv1zelIMUzD2i3t1t0W"


class MinioClient:
    def __init__(self):
        self.client = Minio(
            endpoint="localhost:9002",
            access_key=ACCESS_KEY,
            secret_key=SECRET_KEY,
            secure=False,
        )
        self.bucket_name = "album-arts"

    def dump_image(self, raw_image: str, album_uri: str):
        try:
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=album_uri,
                data=io.BytesIO(raw_image),
                length=len(raw_image),
                content_type="image/png"
            )
            print("Image uploaded successfully!")
        except Exception as e:
            print(f"Error uploading image: {str(e)}")

    def get_object_names(self):
        try:
            objects = self.client.list_objects(
                self.bucket_name, recursive=True)
            object_names = [obj.object_name for obj in objects]
            return object_names

        except Exception as e:
            print(f"Error retrieving object names: {str(e)}")
            return []
