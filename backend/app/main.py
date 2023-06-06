from fastapi import FastAPI
from .services.UserBasedRecommender import UserBasedRecommender
from .repository.SongsRepository import get_database
app = FastAPI()
ub_recommender = UserBasedRecommender()
db = get_database()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test")
def read_item():
    df = ub_recommender.test()
    return {"Pyspark!": df.collect()}
