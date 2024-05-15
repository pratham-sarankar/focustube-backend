from fastapi import APIRouter
from ..services import ChannelSearchService

channel_router = APIRouter()


@channel_router.get("/{id}/info")
def search(id: str):
    channel_search_service = ChannelSearchService(id)
    try:
        result = channel_search_service.get_info()
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "message": str(e)}



@channel_router.get("/{id}/playlists")
async def search(id: str):
    channel_search_service = ChannelSearchService(id)
    try:
        result = channel_search_service.get_playlists()
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "message": str(e)}
