from fastapi import APIRouter, WebSocket
from ..services import PlaylistSearchService
import starlette.websockets
import json

playlist_router = APIRouter()
playlist_search_service = PlaylistSearchService()


@playlist_router.websocket("/search/ws")
async def search(websocket: WebSocket):
    await websocket.accept()
    playlist_search_service.accept(websocket)

    while True:
        try:
            data = await websocket.receive_json()
            command = data.get("command")
            if command == "initial":
                await playlist_search_service.init_search(data['data'], websocket)
            elif command == "next":
                await playlist_search_service.next_search(websocket)
            else:
                await websocket.send_json({"success": False, "message": "Unknown command"})
        except starlette.websockets.WebSocketDisconnect as e:
            playlist_search_service.on_disconnect(websocket)
            break
        except json.JSONDecodeError:
            await websocket.send_json({"success": False, "message": "Invalid JSON"})
        except KeyError as e:
            await websocket.send_json({"success": False, "message": "Either the command or the data is missing"})
            raise e
        except Exception as e:
            await websocket.send_json({"success": False, "message": str(e)})
            raise e

