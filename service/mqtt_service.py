import json
from enum import Enum
from typing import Dict, List

from paho.mqtt import publish

from api.v1.models.washing_machine_model import WashingMachineModel
from mqtt_config import mqtt_broker_ip


class MQTTTopic(str, Enum):
    SERVO = "servo"
    MACHINE_STATUS = "status"


class MqttService:
    async def update_status(self, data: List[WashingMachineModel]) -> Dict:
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

    async def close_door(self, machine_id: str):
        payload = {"machine_id": machine_id, "action": "close"}
        publish.single(
            topic=MQTTTopic.SERVO.value,
            payload=json.dumps(payload),
            hostname=mqtt_broker_ip,
            qos=2,
        )
