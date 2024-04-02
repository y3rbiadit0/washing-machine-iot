import json
from enum import Enum
from functools import cached_property
from typing import Dict, List

from paho.mqtt import publish

from api.v1.models.washing_machine_model import WashingMachineModel
from config import get_config


class MQTTTopic(str, Enum):
    SERVO = "washing_machines_iot/servo"
    MACHINE_STATUS = "washing_machines_iot/status"


class MqttService:
    @cached_property
    def mqtt_ip(self) -> str:
        return get_config().MQTT_SERVER_IP

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
            hostname=self.mqtt_ip,
            qos=2,
        )
        return json_data

    async def open_door(self, machine_id: str):
        payload = {"machine_id": machine_id, "action": "open"}
        publish.single(
            topic=MQTTTopic.SERVO.value,
            payload=json.dumps(payload),
            hostname=self.mqtt_ip,
            qos=2,
        )

    async def close_door(self, machine_id: str):
        payload = {"machine_id": machine_id, "action": "close"}
        publish.single(
            topic=MQTTTopic.SERVO.value,
            payload=json.dumps(payload),
            hostname=self.mqtt_ip,
            qos=2,
        )
