from pydantic import BaseModel


class ReservationResponse(BaseModel):
    valid_until: str
    machine_id: int
    user_id: str


class BaseResponse(BaseModel):
    message: str
    data: ReservationResponse = None
