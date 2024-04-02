import asyncio
import base64
import inspect
import threading
import uuid
from io import BytesIO
from typing import List, Callable

import qrcode
from fastapi import WebSocket

from api.v1.models.washing_machine_model import WashingMachineModel
from .mongo_service import MongoDBService
from ..mqtt_service import MqttService


class WashingMachinesMongoDBService(MongoDBService):
    collection = "washing_machines"
    mqttService = MqttService()

    def __init__(self):
        super().__init__()

    def add(self, data: WashingMachineModel) -> str:
        data.machine_id = str(uuid.uuid4())
        data.status = "free"
        data.qr_code = self._generate_qr_code(data)
        return super().add(data.model_dump())

    def update(self, machine_id: str, data: dict) -> str:
        doc_id = self.get_doc_id_by_field(field="machine_id", expected_value=machine_id)
        return super().update(doc_id, data)

    def get(self, doc_id: str) -> WashingMachineModel:
        return WashingMachineModel(**super().get(doc_id))

    def get_by_machine_id(self, machine_id: str) -> WashingMachineModel:
        return WashingMachineModel(
            **super().get_by_field(field="machine_id", expected_value=machine_id)
        )

    def get_all(self) -> List[WashingMachineModel]:
        return [WashingMachineModel(**doc) for doc in super().get_all()]

    def _generate_qr_code(self, data: WashingMachineModel) -> str:
        # Generate a QR code with the washing machine ID
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"washing_machine_id={data.machine_id}; model={data.model} ")
        qr.make(fit=True)

        # Create an image from the QR code
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image to a BytesIO object
        img_bytes_io = BytesIO()
        img.save(img_bytes_io)
        img_bytes_io.seek(0)

        return base64.b64encode(img_bytes_io.read()).decode("utf-8")

    def listen_to_changes(self, websocket: WebSocket):
        async def _on_snapshot():
            collection = list(WashingMachinesMongoDBService().collection_ref.find({}))
            data = [WashingMachineModel(**doc) for doc in collection]
            json_data = [data.model_dump() for data in data]
            await MqttService().update_status(data)
            await websocket.send_json(json_data, mode="text")

        WashingMachinesListener(_on_snapshot).start()


class WashingMachinesListener(threading.Thread):
    def __init__(self, on_snapshot: Callable):
        super(WashingMachinesListener, self).__init__()
        self.on_snapshot = on_snapshot

    def run(self):
        if inspect.iscoroutinefunction(self.on_snapshot):
            asyncio.run(self.on_snapshot())
        else:
            self.on_snapshot()
        with WashingMachinesMongoDBService().collection_ref.watch(
            full_document="updateLookup"
        ) as stream:
            while stream.alive:
                change = stream.try_next()
                if change is not None:
                    if inspect.iscoroutinefunction(self.on_snapshot):
                        asyncio.run(self.on_snapshot())
                    else:
                        self.on_snapshot()
                    continue
