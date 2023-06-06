from pymongo import MongoClient
import os


def get_database():
    client = MongoClient(os.environ["DATABASE_URL"])
    return client['songs']


if __name__ == "__main__":
    dbname = get_database()
