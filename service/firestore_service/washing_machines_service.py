import base64
import uuid
from io import BytesIO
from typing import List

import qrcode
from fastapi import WebSocket

from api.v1.models.washing_machine_model import WashingMachineModel
from .firestore_service import FirestoreService


class WashingMachinesFirestoreService(FirestoreService):
    collection = "washing_machines"

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

    async def listen_washing_machines(self, websocket: WebSocket):
        async def on_snapshot(doc_snapshot, changes, read_time):
            data = [
                WashingMachineModel(**doc.to_dict()).model_dump()
                for doc in doc_snapshot
            ]
            await websocket.send_json(data, mode="text")

        doc_watch = self.collection_ref.on_snapshot(on_snapshot)

        try:
            # IMPORTANT: Keep WebSocket connection alive
            while True:
                await websocket.receive_text()
        except Exception as e:
            doc_watch.unsubscribe()
