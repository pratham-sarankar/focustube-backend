from fastapi import APIRouter
from ..services import CommentSearchService

comment_router = APIRouter()


@comment_router.get("/{id}")
def search(id: str):
    try:
        result = CommentSearchService(id).search()
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "message": str(e)}
