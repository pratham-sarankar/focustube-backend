from fastapi import WebSocket
from youtubesearchpython import CustomSearch


class SearchConnection:
    def __init__(self, websocket: WebSocket, search_obj: CustomSearch | None):
        self.websocket = websocket
        self.search_obj = search_obj
