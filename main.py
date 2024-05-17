from fastapi import FastAPI
from app.search import focustube_router, playlist_router, channel_router, comment_router

app = FastAPI()

app.include_router(focustube_router)
app.include_router(playlist_router, prefix="/playlist")
app.include_router(channel_router, prefix="/channel")
app.include_router(comment_router, prefix="/comment")
