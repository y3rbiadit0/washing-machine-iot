import json
from enum import Enum
from typing import Dict

from paho.mqtt import publish

from mqtt_config import mqtt_broker_ip
from .firestore_service.washing_machines_service import WashingMachinesFirestoreService


class MQTTTopic(str, Enum):
    SERVO = "servo"
    MACHINE_STATUS = "status"


class MqttService:
    washing_machines_firestore_service: WashingMachinesFirestoreService = None

    def __init__(self):
        self.washing_machines_firestore_service = WashingMachinesFirestoreService()

    async def update_status(self) -> Dict:
        data = self.washing_machines_firestore_service.get_all()
        free_machines = len(
            [
                washing_machine
                for washing_machine in data
                if washing_machine.status == "free"
            ]
        )
        occupied_machines = len(
            [
                washing_machine
                for washing_machine in data
                if washing_machine.status == "occupied"
            ]
        )
        out_of_service_machines = len(
            [
                washing_machine
                for washing_machine in data
                if washing_machine.status == "out_of_service"
            ]
        )
        json_data = {
            "free": free_machines,
            "occupied": occupied_machines,
            "out_of_service": out_of_service_machines,
        }

        publish.single(
            topic=MQTTTopic.MACHINE_STATUS.value,
            payload=json.dumps(json_data),
            hostname=mqtt_broker_ip,
            qos=2,
        )
        return json_data

    async def open_door(self, machine_id: str):
        payload = {"machine_id": machine_id, "action": "open"}
        publish.single(
            topic=MQTTTopic.SERVO.value,
            payload=json.dumps(payload),
            hostname=mqtt_broker_ip,
            qos=2,
        )
        return {"message": "Door Opened!"}

    async def close_door(self, machine_id: str):
        payload = {"machine_id": machine_id, "action": "close"}
        publish.single(
            topic=MQTTTopic.SERVO.value,
            payload=json.dumps(payload),
            hostname=mqtt_broker_ip,
            qos=2,
        )
        return {"message": "Door Closed!"}
