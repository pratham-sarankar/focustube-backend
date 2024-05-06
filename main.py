import json

import starlette.websockets
from fastapi import FastAPI, WebSocket
from youtubesearchpython import VideosSearch, Video, ResultMode, Suggestions
import uuid

app = FastAPI()

connected_users = {}


@app.get("/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}"}


@app.get("/video/{video_id}")
def get_video(video_id: str):
    data = Video.getInfo(f'https://youtu.be/{video_id}', mode=ResultMode.json)
    return data


@app.get("/suggestions/{query}")
def search(query: str):
    return Suggestions(language='en', region='US').get(query, mode=ResultMode.dict)


@app.websocket("/search/ws")
async def search(websocket: WebSocket):
    await websocket.accept()
    handle_connections(websocket)

    while True:
        try:
            data = await websocket.receive_json()
            command = data.get("command")
            if command == "initial":
                await init_search(data, websocket)
            elif command == "next":
                await next_search(websocket)
            else:
                await websocket.send_json({"success": False, "message": "Unknown command"})
        except starlette.websockets.WebSocketDisconnect as e:
            user_id = next(key for key, value in connected_users.items() if value["websocket"] == websocket)
            if user_id in connected_users:  # Check if user ID exists before deletion
                del connected_users[user_id]
            print(f"Connection closed by client: {user_id}")
            break
        except json.JSONDecodeError:
            await websocket.send_json({"success": False, "message": "Invalid JSON"})
        except KeyError:
            await websocket.send_json({"success": False, "message": "Eith er the command or the data is missing"})
        except Exception as e:
            await websocket.send_json({"success": False, "message": str(e)})
            raise e


def handle_connections(websocket: WebSocket):
    user_id = str(uuid.uuid4())
    search_obj = None
    connected_users[user_id] = {"websocket": websocket, "search_obj": search_obj}


async def init_search(data, websocket: WebSocket):
    user_id = next(key for key, value in connected_users.items() if value["websocket"] == websocket)
    search_obj: VideosSearch = VideosSearch(data['data']['q'], limit=10)
    connected_users[user_id]["search_obj"] = search_obj
    results = search_obj.result()
    await websocket.send_json({"success": True, "data": results['result']})


async def next_search(websocket: WebSocket):
    user_id = next(key for key, value in connected_users.items() if value["websocket"] == websocket)
    search_obj: VideosSearch = connected_users[user_id]["search_obj"]
    search_obj.next()
    results = search_obj.result()
    await websocket.send_json({"success": True, "data": results['result']})
