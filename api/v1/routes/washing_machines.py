import base64
import http
from io import BytesIO
from typing import List

from fastapi import APIRouter, WebSocket
from starlette.responses import StreamingResponse

from service.firestore_service.reservation_service import ReservationFirestoreService
from service.firestore_service.washing_machines_service import (
    WashingMachinesFirestoreService,
)
from service.mqtt_service import MqttService
from ..models.base_response import BaseResponse
from ..models.reservation_model import ReservationModel
from ..models.washing_machine_model import WashingMachineModel

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


@router.post("/unblock", status_code=http.HTTPStatus.CREATED)
async def unblock_machine(reservation_data: ReservationModel):
    await MqttService().open_door(machine_id=reservation_data.machine_id)
    return BaseResponse(message="Machine unblocked successfully!")


@router.post("/block", status_code=http.HTTPStatus.CREATED)
async def block_machine(reservation_data: ReservationModel):
    await MqttService().close_door(machine_id=reservation_data.machine_id)
    return BaseResponse(message="Machine blocked successfully!")


@router.post("/reserve", status_code=http.HTTPStatus.CREATED)
async def reserve_washing_machine() -> ReservationModel:
    reservation_service = ReservationFirestoreService()
    reservation_id = reservation_service.add({"user_id": "dummy_user_id"})
    reservation = reservation_service.get(reservation_id)
    await MqttService().update_status()
    return reservation


@router.websocket("/washing-machines-ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await WashingMachinesFirestoreService().listen_washing_machines(websocket)


@router.websocket("/reservation-ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await ReservationFirestoreService().listen_reservations(websocket)
