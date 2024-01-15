from typing import Literal

from pydantic import BaseModel


class ReservationModel(BaseModel):
    machine_id: str = None
    user_id: str = None
    reservation_id: str = None
    limit_time: str = None
    reservation_status: Literal[
        "created", "clothes_loaded", "not_used", "finished"
    ] = None
