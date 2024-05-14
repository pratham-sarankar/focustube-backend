from fastapi import WebSocket
from youtubesearchpython import Playlist


class PlaylistSearchConnection:
    def __init__(self, websocket: WebSocket, search_obj: Playlist | None):
        self.websocket = websocket
        self.search_obj = search_obj
