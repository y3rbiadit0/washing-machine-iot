import base64
import http
from io import BytesIO
from typing import List

from fastapi import APIRouter
from starlette.responses import StreamingResponse

from service.firestore_service.reservation_service import (
    ReservationFirestoreService,
    ReservationModel,
)
from service.firestore_service.washing_machines_service import (
    WashingMachinesFirestoreService,
    WashingMachineModel,
)

router = APIRouter(prefix="/washing-machines")


@router.post("/", status_code=http.HTTPStatus.CREATED)
async def add_new_machine(data: WashingMachineModel):
    return {"id": WashingMachinesFirestoreService().add(data)}


@router.get("/status/{machine_id}", status_code=http.HTTPStatus.OK)
async def get_machine_status(machine_id: str) -> WashingMachineModel:
    data = WashingMachinesFirestoreService().get_by_machine_id(machine_id=machine_id)
    return data


@router.get("/all", status_code=http.HTTPStatus.OK)
async def get_machines_data() -> List[WashingMachineModel]:
    data = WashingMachinesFirestoreService().get_all()
    return data


@router.get("/qr_code/{machine_id}", status_code=http.HTTPStatus.OK)
async def get_qr_code(machine_id: str) -> StreamingResponse:
    qr_code_bytes = (
        WashingMachinesFirestoreService()
        .get_by_machine_id(machine_id=machine_id)
        .qr_code
    )
    # Return the QR code bytes as a StreamingResponse
    return StreamingResponse(
        BytesIO(base64.b64decode(qr_code_bytes)), media_type="image/png"
    )


@router.post("/start", status_code=http.HTTPStatus.CREATED)
async def start_laundry():
    # Reserve washing machine

    # Publish to topic -> new status of machines
    # Send message to servo to open door
    return {"message": "Start Successful!"}


@router.post("/end", status_code=http.HTTPStatus.OK)
async def end_laundry():
    # Free washing machine
    # Publish to topic -> new status of machines
    # Send message to servo to open door
    return {"message": "Cancellation Successful!"}


@router.post("/reserve", status_code=http.HTTPStatus.CREATED)
async def reserve_washing_machine() -> ReservationModel:
    reservation_service = ReservationFirestoreService()
    reservation_id = reservation_service.add({"user_id": "dummy_user_id"})
    reservation = reservation_service.get(reservation_id)
    return reservation
