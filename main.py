from fastapi import FastAPI
from app.search import focustube_router

app = FastAPI()

app.include_router(focustube_router)
