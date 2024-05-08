from fastapi import APIRouter, WebSocket
from youtubesearchpython import Video, Suggestions, ResultMode
import starlette.websockets
from ..services import FocusTubeSearchService
import json

focustube_router = APIRouter()
focustube_search_service = FocusTubeSearchService()


@focustube_router.get("/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}"}


@focustube_router.get("/video/{video_id}")
def get_video(video_id: str):
    data = Video.getInfo(f'https://youtu.be/{video_id}', mode=ResultMode.json)
    return data


@focustube_router.get("/suggestions/{query}")
def search(query: str):
    return Suggestions(language='en', region='US').get(query, mode=ResultMode.dict)


@focustube_router.websocket("/search/ws")
async def search(websocket: WebSocket):
    await websocket.accept()
    focustube_search_service.accept(websocket)

    while True:
        try:
            data = await websocket.receive_json()
            command = data.get("command")
            if command == "initial":
                await focustube_search_service.init_search(data['data'], websocket)
            elif command == "next":
                await focustube_search_service.next_search(websocket)
            else:
                await websocket.send_json({"success": False, "message": "Unknown command"})
        except starlette.websockets.WebSocketDisconnect as e:
            focustube_search_service.on_disconnect(websocket)
            break
        except json.JSONDecodeError:
            await websocket.send_json({"success": False, "message": "Invalid JSON"})
        except KeyError as e:
            await websocket.send_json({"success": False, "message": "Either the command or the data is missing"})
            raise e
        except Exception as e:
            await websocket.send_json({"success": False, "message": str(e)})
            raise e
