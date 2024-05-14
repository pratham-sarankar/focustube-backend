import uuid
from fastapi import WebSocket
from ..models.channel_search.channel_search_connection import ChannelSearchConnection
from youtubesearchpython import Playlist, playlist_from_channel_id


class ChannelSearchService:
    def __init__(self, ):
        self.connected_users: dict = {}

    def accept(self, websocket: WebSocket):
        user_id = str(uuid.uuid4())
        self.connected_users[user_id] = ChannelSearchConnection(websocket, None)
        pass

    async def init_search(self, data, websocket: WebSocket):
        try:
            # Fetch user_id from connected_users
            user_id = next(key for key, value in self.connected_users.items() if value.websocket == websocket)

            # Validate Search Preferences
            search_obj: Playlist = Playlist(playlist_from_channel_id(data['id']))
            self.connected_users[user_id].search_obj = search_obj
            await websocket.send_json({"success": True, "data": search_obj.videos})
        except ValueError as e:
            await websocket.send_json({"success": False, "message": str(e)})

    async def next_search(self, websocket: WebSocket):
        user_id = next(key for key, value in self.connected_users.items() if value.websocket == websocket)
        search_obj: Playlist | None = self.connected_users[user_id].search_obj
        if search_obj is None:
            await websocket.send_json({"success": False, "message": "No search object found"})
            return
        else:
            search_obj.getNextVideos()
            await websocket.send_json({"success": True, "data": search_obj.videos})

    def on_disconnect(self, websocket: WebSocket):
        user_id = next(key for key, value in self.connected_users.items() if value.websocket == websocket)
        if user_id in self.connected_users:  # Check if user ID exists before deletion
            del self.connected_users[user_id]
        print(f"Connection closed by client: {user_id}")
