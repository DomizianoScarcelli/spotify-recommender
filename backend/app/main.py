from fastapi import FastAPI
from .services.recommendations.UserBasedRecommender import UserBasedRecommender
from .api.routes import router
app = FastAPI()

app.include_router(router)
