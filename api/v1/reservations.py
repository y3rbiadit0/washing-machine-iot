import http

from fastapi import APIRouter

from api.v1.models.base_response import ReservationResponse, BaseResponse

router = APIRouter(prefix="/reservation")


@router.post("", status_code=http.HTTPStatus.CREATED)
async def new_reservation() -> BaseResponse:
    return BaseResponse(
        message="Reservation Successful!",
        data=ReservationResponse(
            status=True,
            message="Reservation Successful!",
            valid_until="2023-01-01T00:00:00Z",
            machine_id="2",
            user_id="1",
        ),
    )


@router.delete("", status_code=http.HTTPStatus.CREATED)
async def cancel_reservation():
    return {
        "valid_until": "2023-01-01T00:00:00Z",
        "machine_id": 1,
        "user_id": 1,
        "status": "free",
    }
