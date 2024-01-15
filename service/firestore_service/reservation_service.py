import datetime
import uuid
from random import randint
from typing import Dict, List

from fastapi import WebSocket

from api.v1.models.reservation_model import ReservationModel
from .firestore_service import FirestoreService
from .washing_machines_service import (
    WashingMachinesFirestoreService,
)
from ..helpers import datetime_helper


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
            reservation_status="created",
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

    def get_all(self) -> List[ReservationModel]:
        return [ReservationModel(**doc) for doc in super().get_all()]

    async def listen_reservations(self, websocket: WebSocket):
        doc_ref = self.collection_ref

        async def on_snapshot(doc_snapshot, changes, read_time):
            data = [
                ReservationModel(**doc.to_dict()).model_dump() for doc in doc_snapshot
            ]
            await websocket.send_json(data, mode="text")

        doc_watch = doc_ref.on_snapshot(on_snapshot)

        try:
            # IMPORTANT: Keep WebSocket connection alive
            while True:
                await websocket.receive_text()
        except Exception as e:
            doc_watch.unsubscribe()

    def update(self, reservation_id: str, data: dict) -> str:
        doc_id = self.get_doc_id_by_field(
            field="reservation_id", expected_value=reservation_id
        )
        self.collection_ref.document(doc_id).update(data)
        return doc_id
