import http
from io import BytesIO

from fastapi import APIRouter
from starlette.responses import StreamingResponse

from service.firestore_service.washing_machines_service import (
    WashingMachinesFirestoreService,
    WashingMachineModel,
)

router = APIRouter(prefix="/washing-machines")


@router.post("/", status_code=http.HTTPStatus.CREATED)
async def add_new_machine(data: WashingMachineModel):
    return {"id": WashingMachinesFirestoreService().add(data)}


@router.get("/", status_code=http.HTTPStatus.OK)
async def get_machines_status() -> WashingMachineModel:
    data = WashingMachinesFirestoreService().get(doc_id="a5IgkOocZeqI0WkaPMZH")
    return data

@router.get("/all", status_code=http.HTTPStatus.OK)
async def get_machines_status() -> WashingMachineModel:
    data = WashingMachinesFirestoreService().get(doc_id="a5IgkOocZeqI0WkaPMZH")
    return data


@router.get("/get_qr_code")
async def get_qr_code():
    qr_code_bytes = (
        WashingMachinesFirestoreService().get(doc_id="a5IgkOocZeqI0WkaPMZH").qr_code
    )

    # Return the QR code bytes as a StreamingResponse
    return StreamingResponse(BytesIO(qr_code_bytes), media_type="image/png")


@router.post("/start", status_code=http.HTTPStatus.CREATED)
async def start_laundry():
    return {"message": "Start Successful!"}


@router.post("/end", status_code=http.HTTPStatus.OK)
async def end_laundry():
    return {"message": "Cancellation Successful!"}
