import json
from typing import Dict, TypeVar, List

from pymongo import MongoClient
from pymongo.collection import Collection

T = TypeVar("T")


class MongoDBService:
    client: MongoClient = MongoClient(
        "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&replicaSet=dbrs"
    )
    db_name: str = "washing_machines_db"
    collection: str
    collection_ref: Collection

    def __init__(self):
        self.db = self.client[self.db_name]
        self.collection_ref = self.db[self.collection]

    @staticmethod
    def init_db():
        db_client = MongoDBService.client
        db_client.drop_database(MongoDBService.db_name)
        db = db_client[MongoDBService.db_name]
        db.create_collection("reservations")
        db.create_collection("washing_machines")
        with open("db/init_data.json") as f:
            washing_machines_init_data = json.load(f)
            db["washing_machines"].insert_many(washing_machines_init_data)

    def add(self, data: T) -> str:
        result = self.collection_ref.insert_one(data)
        return result.inserted_id

    def get(self, doc_id: str) -> T:
        result = self.collection_ref.find_one({"_id": doc_id})
        return result

    def get_doc_id_by_field(self, field: str, expected_value: str) -> str:
        result = self.collection_ref.find_one({field: expected_value})
        return result.get("_id")

    def get_by_field(self, field: str, expected_value: str) -> T:
        result = self.collection_ref.find_one({field: expected_value})
        return result

    def get_multiple_by_field(self, field: str, expected_value: str) -> List[Dict]:
        results = self.collection_ref.find({field: expected_value})
        return list(results)

    def get_all(self) -> List[T]:
        docs = self.collection_ref.find({})
        return list(docs)

    def update(self, doc_id: str, data: dict) -> str:
        result = self.collection_ref.update_one(
            filter={"_id": doc_id}, update={"$set": data}
        )
        return doc_id

    def delete(self, doc_id: str) -> str:
        result = self.collection_ref.delete_one({"_id": doc_id})
        return doc_id
