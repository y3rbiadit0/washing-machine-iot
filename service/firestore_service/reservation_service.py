import datetime
import uuid
from dataclasses import dataclass
from random import randint
from typing import Dict

from pydantic import BaseModel

from .firestore_service import FirestoreService
from .washing_machines_service import (
    WashingMachinesFirestoreService,
)
from ..helpers import datetime_helper


class ReservationModel(BaseModel):
    machine_id: str = None
    user_id: str = None
    reservation_id: str = None
    limit_time: str = None


class ReservationFirestoreService(FirestoreService):
    collection = "reservations"

    def add(self, data: Dict) -> str:
        selected_washing_machine_id = self._reserve_washing_machine()
        limit_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
        reservation_id = str(uuid.uuid4())
        data = ReservationModel(
            reservation_id=reservation_id,
            user_id=data["user_id"],
            machine_id=selected_washing_machine_id,
            limit_time=datetime_helper.datetime_to_str(limit_time),
        )
        firestore_id = super().add(data.model_dump())
        return firestore_id

    def _reserve_washing_machine(self) -> str:
        washing_machine_service = WashingMachinesFirestoreService()
        available_washing_machines = washing_machine_service.get_multiple_by_field(
            "status", "free"
        )
        if len(available_washing_machines) == 0:
            raise Exception("No washing machines available")
        selected_washing_machine = available_washing_machines[
            randint(0, len(available_washing_machines) - 1)
        ]
        washing_machine_service.update(
            selected_washing_machine["machine_id"], data={"status": "occupied"}
        )
        return selected_washing_machine["machine_id"]

    def get(self, doc_id: str) -> ReservationModel:
        return ReservationModel(**super().get(doc_id))
