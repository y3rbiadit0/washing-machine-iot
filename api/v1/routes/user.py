import http

from fastapi import APIRouter

router = APIRouter(prefix="/users")


@router.post("", status_code=http.HTTPStatus.CREATED)
async def register_new_user():
    # TODO: Implement logic to accept only UNISA Emails and whitelisted.
    return {"message": "Login Successfully!"}


@router.delete("", status_code=http.HTTPStatus.CREATED)
async def delete_user():
    # TODO: Implement logic to accept only UNISA Emails and whitelisted.
    return {"message": "Login Successfully!"}
