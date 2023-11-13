import http

from fastapi import APIRouter

router = APIRouter(prefix="/washing-machines")


@router.post("/feedback", status_code=http.HTTPStatus.CREATED)
async def feedback():
    return {"message": "Thanks for the feedback !"}
