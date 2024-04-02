import json
from typing import Dict, TypeVar, List

from pymongo import MongoClient
from pymongo.collection import Collection

from definitions import ROOT_DIR

T = TypeVar("T")


class MongoDBService:
    collection_ref: Collection
    collection: str
    db_name: str = "washing_machines_db"
    mongo_db_url: str = "mongodb://localhost:27017/?directConnection=true&serverSelectionTimeoutMS=2000&replicaSet=dbrs"

    def __init__(
        self,
        client: MongoClient = MongoClient(mongo_db_url),
    ):
        self.client = client
        self.db = self.client[self.db_name]
        self.collection_ref = self.db[self.collection]

    @staticmethod
    def init_db(
        client: MongoClient = MongoClient(mongo_db_url),
    ):
        """Init the database with the initial data."""
        client.drop_database(MongoDBService.db_name)
        db = client[MongoDBService.db_name]
        db.create_collection("reservations")
        db.create_collection("washing_machines")
        with open(f"{ROOT_DIR}/db/init_data.json") as f:
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
