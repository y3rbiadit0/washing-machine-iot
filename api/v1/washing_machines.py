import http

from fastapi import APIRouter

router = APIRouter(prefix="/washing-machines")


@router.post("/add-new-machine", status_code=http.HTTPStatus.CREATED)
async def add_new_machine():
    return {"message": "Machines Status!"}

@router.get("/get-machines-status", status_code=http.HTTPStatus.OK)
async def get_machines_status():
    return {"message": "Machines Status!"}
@router.post("/start", status_code=http.HTTPStatus.CREATED)
async def start_laundry():
    return {"message": "Start Successful!"}

@router.post("/end", status_code=http.HTTPStatus.OK)
async def end_laundry():
    return {"message": "Cancellation Successful!"}

