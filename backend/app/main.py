from fastapi import FastAPI
from .services.UserBasedRecommender import UserBasedRecommender
app = FastAPI()
ub_recommender = UserBasedRecommender()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test")
def read_item():
    df = ub_recommender.test()
    return {"Pyspark!": df.collect()}
