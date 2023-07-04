from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from fastapi import FastAPI
import os

app = FastAPI()
print(os.environ)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    # Replace "*" with the specific origins you want to allow
    allow_origins=["*"],
    # Replace "*" with the specific HTTP methods you want to allow
    allow_methods=["*"],
    # Replace "*" with the specific headers you want to allow
    allow_headers=["*"],
)
