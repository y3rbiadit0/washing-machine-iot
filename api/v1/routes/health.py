import http

from fastapi import APIRouter

router = APIRouter(prefix="/health")


@router.get("", status_code=http.HTTPStatus.OK)
async def health():
    return {"status": "ok"}
