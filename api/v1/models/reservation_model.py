from pydantic import BaseModel


class ReservationModel(BaseModel):
    machine_id: str = None
    user_id: str = None
    reservation_id: str = None
    limit_time: str = None
