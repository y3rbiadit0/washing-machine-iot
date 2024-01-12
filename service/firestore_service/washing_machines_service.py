import base64
import uuid
from io import BytesIO
from typing import List, Literal

import qrcode
from pydantic import BaseModel

from .firestore_service import FirestoreService


class WashingMachineModel(BaseModel):
    machine_id: str = None
    location: str
    capacity_kg: int
    price: int = 0
    status: Literal["free", "occupied", "out_of_service"] = "free"
    qr_code: str = None
    brand: str = None
    model: str = None


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
