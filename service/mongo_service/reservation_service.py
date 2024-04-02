import asyncio
import datetime
import inspect
import threading
import uuid
from random import randint
from typing import Dict, List, Callable

from fastapi import WebSocket

from api.v1.models.reservation_model import ReservationModel
from .mongo_service import MongoDBService
from .washing_machines_service import (
    WashingMachinesMongoDBService,
)
from ..helpers import datetime_helper


class ReservationMongoDBService(MongoDBService):
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
        washing_machine_service = WashingMachinesMongoDBService()
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

    def update(self, reservation_id: str, data: dict) -> str:
        doc_id = self.get_doc_id_by_field(
            field="reservation_id", expected_value=reservation_id
        )
        return super().update(doc_id, data)

    def delete(self, reservation_id: str) -> str:
        doc_id = self.get_doc_id_by_field(
            field="reservation_id", expected_value=reservation_id
        )
        return super().delete(doc_id)

    def listen_to_changes(self, websocket: WebSocket):
        async def _on_snapshot():
            data = [reservation.model_dump() for reservation in self.get_all()]
            await websocket.send_json(data, mode="text")

        ReservationsListener(on_snapshot=_on_snapshot).start()


class ReservationsListener(threading.Thread):
    def __init__(self, on_snapshot: Callable):
        super(ReservationsListener, self).__init__()
        self.on_snapshot = on_snapshot

    def run(self):
        if inspect.iscoroutinefunction(self.on_snapshot):
            asyncio.run(self.on_snapshot())
        else:
            self.on_snapshot()

        with ReservationMongoDBService().collection_ref.watch(
            full_document="updateLookup"
        ) as stream:
            while stream.alive:
                change = stream.try_next()
                if change is not None:
                    if inspect.iscoroutinefunction(self.on_snapshot):
                        asyncio.run(self.on_snapshot())
                    else:
                        self.on_snapshot()
                    continue
