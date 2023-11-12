import http

from fastapi import APIRouter

router = APIRouter(prefix="/auth")


@router.post("/login", status_code=http.HTTPStatus.OK)
async def login():
    # TODO: Implement logic to accept only UNISA Emails and whitelisted.
    return {"message": "Login Successfully!"}
