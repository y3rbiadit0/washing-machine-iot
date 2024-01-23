import asyncio
import base64
import http
import threading
from io import BytesIO
from typing import List

from fastapi import APIRouter, WebSocket
from starlette.responses import StreamingResponse

from service.mongo_service.reservation_service import ReservationMongoDBService
from service.mongo_service.washing_machines_service import WashingMachinesMongoDBService
from service.mqtt_service import MqttService
from ..models.base_response import BaseResponse
from ..models.reservation_model import ReservationModel
from ..models.washing_machine_model import WashingMachineModel

router = APIRouter(prefix="/washing-machines")


@router.post("/", status_code=http.HTTPStatus.CREATED)
async def add_new_machine(data: WashingMachineModel):
    return {"id": WashingMachinesMongoDBService().add(data)}


@router.get("/status/{machine_id}", status_code=http.HTTPStatus.OK)
async def get_machine_status(machine_id: str) -> WashingMachineModel:
    data = WashingMachinesMongoDBService().get_by_machine_id(machine_id=machine_id)
    return data


@router.get("/all", status_code=http.HTTPStatus.OK)
async def get_machines_data() -> List[WashingMachineModel]:
    data = WashingMachinesMongoDBService().get_all()
    return data


@router.get("/qr_code/{machine_id}", status_code=http.HTTPStatus.OK)
async def get_qr_code(machine_id: str) -> StreamingResponse:
    qr_code_bytes = (
        WashingMachinesMongoDBService().get_by_machine_id(machine_id=machine_id).qr_code
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
    reservation_service = ReservationMongoDBService()
    await MqttService().close_door(machine_id=reservation_data.machine_id)
    if reservation_data.reservation_status == "created":
        reservation_service.update(
            reservation_id=reservation_data.reservation_id,
            data={"reservation_status": "clothes_loaded"},
        )
    if reservation_data.reservation_status == "clothes_loaded":
        reservation_service.update(
            reservation_id=reservation_data.reservation_id,
            data={"reservation_status": "finished"},
        )
        WashingMachinesMongoDBService().update(
            reservation_data.machine_id, data={"status": "free"}
        )
        reservation_service.delete(reservation_data.reservation_id)

    return BaseResponse(message="Machine blocked successfully!")


@router.post("/reserve", status_code=http.HTTPStatus.CREATED)
async def reserve_washing_machine() -> ReservationModel:
    reservation_service = ReservationMongoDBService()
    reservation_id = reservation_service.add({"user_id": "dummy_user_id"})
    reservation = reservation_service.get(reservation_id)
    return reservation


class WashingMachinesListenerThread(threading.Thread):
    def __init__(self, websocket: WebSocket):
        super(WashingMachinesListenerThread, self).__init__()
        self.websocket = websocket

    def run(self):
        with WashingMachinesMongoDBService().collection_ref.watch(
            full_document="updateLookup"
        ) as stream:
            while stream.alive:
                change = stream.try_next()
                if change is not None:
                    collection = list(
                        WashingMachinesMongoDBService().collection_ref.find({})
                    )
                    data = [WashingMachineModel(**doc) for doc in collection]
                    json_data = [data.model_dump() for data in data]
                    asyncio.run(MqttService().update_status(data))
                    asyncio.run(self.websocket.send_json(json_data, mode="text"))
                    continue


@router.websocket("/washing-machines-ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    WashingMachinesListenerThread(websocket).start()
    try:
        await websocket.receive_text()
    except Exception as e:
        pass


# @router.websocket("/reservation-ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     await ReservationFirestoreService().listen_reservations(websocket)
