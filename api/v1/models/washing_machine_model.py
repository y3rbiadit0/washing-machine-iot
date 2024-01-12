from typing import Literal

from pydantic import BaseModel


class WashingMachineModel(BaseModel):
    machine_id: str = None
    location: str
    capacity_kg: int
    price: int = 0
    status: Literal["free", "occupied", "out_of_service"] = "free"
    qr_code: str = None
    brand: str = None
    model: str = None
