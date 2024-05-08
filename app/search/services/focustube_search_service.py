from fastapi import WebSocket
from youtubesearchpython import CustomSearch
from app.search.models.search_connection import SearchConnection
from app.search.models.enums import SearchType, UploadDateFilter, SortOrder
from app.search.models.search_preference import SearchPreference
import uuid


class FocusTubeSearchService:
    def __init__(self, ):
        self.connected_users: dict = {}

    def accept(self, websocket: WebSocket):
        user_id = str(uuid.uuid4())
        self.connected_users[user_id] = SearchConnection(websocket, None)
        pass

    async def init_search(self, data, websocket: WebSocket):
        try:
            # Fetch user_id from connected_users
            user_id = next(key for key, value in self.connected_users.items() if value.websocket == websocket)

            # Validate Search Preferences
            print(data)
            search_type = SearchType(data['type']) if 'type' in data else None
            search_filter = UploadDateFilter(data['filter']) if (
                    'filter' in data and data['filter'] is not None) else None
            search_order = SortOrder(data['order']) if 'order' in data else SortOrder.relevance

            search_preference = SearchPreference(search_type, search_filter, search_order)
            sp_code = search_preference.get_code()

            search_obj: CustomSearch = CustomSearch(data['q'], sp_code, limit=10)
            self.connected_users[user_id].search_obj = search_obj
            results = search_obj.result()
            await websocket.send_json({"success": True, "data": results['result']})
        except ValueError as e:
            await websocket.send_json({"success": False, "message": str(e)})

    async def next_search(self, websocket: WebSocket):
        user_id = next(key for key, value in self.connected_users.items() if value.websocket == websocket)
        search_obj: CustomSearch = self.connected_users[user_id].search_obj
        search_obj.next()
        results = search_obj.result()
        await websocket.send_json({"success": True, "data": results['result']})

    def on_disconnect(self, websocket: WebSocket):
        user_id = next(key for key, value in self.connected_users.items() if value.websocket == websocket)
        if user_id in self.connected_users:  # Check if user ID exists before deletion
            del self.connected_users[user_id]
        print(f"Connection closed by client: {user_id}")
