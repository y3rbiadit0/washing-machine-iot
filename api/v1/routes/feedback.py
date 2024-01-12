import http

from fastapi import APIRouter

router = APIRouter(prefix="/feedback")


@router.post("", status_code=http.HTTPStatus.CREATED)
async def feedback():
    return {"message": "Thanks for the feedback !"}
