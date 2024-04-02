import json
from functools import cached_property
from typing import Dict, TypeVar, List, Any, Mapping

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

import config
from definitions import ROOT_DIR

T = TypeVar("T")


class MongoDBService:
    collection_ref: Collection
    collection: str
    db_name: str = "washing_machines_db"

    @cached_property
    def db(self) -> Database[Mapping[str, Any] | Any]:
        return self.client()[self.db_name]
    @cached_property
    def collection_ref(self) -> Collection:
        return self.db[self.collection]


    def client(self) -> MongoClient:
        mongo_uri = config.get_config().MONGO_URL
        return MongoClient(mongo_uri)

    def reset_db_data(self):
        """Init the database with the initial data."""
        self.client().drop_database(MongoDBService.db_name)
        db = self.client()[MongoDBService.db_name]
        db.create_collection("reservations")
        db.create_collection("washing_machines")
        with open(f"{ROOT_DIR}/db/init_data.json") as f:
            washing_machines_init_data = json.load(f)
            db["washing_machines"].insert_many(washing_machines_init_data)

    def add(self, data: T) -> str:
        result = self.collection_ref.insert_one(data)
        return str(result.inserted_id)

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
