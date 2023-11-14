import http

from fastapi import APIRouter

from api.v1.models.base_response import ReservationResponse, BaseResponse
from service.firestore_service import ReservationFirestoreService

router = APIRouter(prefix="/reservation")


@router.post("", status_code=http.HTTPStatus.CREATED)
async def new_reservation() -> BaseResponse:
    # Replace the following with the actual data for your reservation
    reservation_data = {
        "user_id": "123456",
        "room_id": "A101",
        "check_in": "2023-01-01T00:00:00Z",
        "guests": 2,
    }

    id = ReservationFirestoreService().add(reservation_data)

    print(f"Reservation added with ID: {id}")

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
