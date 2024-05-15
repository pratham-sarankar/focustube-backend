from fastapi import WebSocket
from youtubesearchpython import Channel


class ChannelSearchConnection:
    def __init__(self, websocket: WebSocket, search_obj: Channel | None):
        self.websocket = websocket
        self.search_obj = search_obj
