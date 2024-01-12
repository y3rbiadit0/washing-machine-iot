from typing import TypeVar, List

from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter

T = TypeVar("T")


class FirestoreService:
    collection: str

    def __init__(self):
        self.db = firestore.client()
        self.collection_ref = self.db.collection(self.collection)

    def add(self, data: T) -> str:
        timestamp, doc_ref = self.collection_ref.add(data)
        return doc_ref.id

    def get(self, doc_id: str) -> T:
        doc = self.collection_ref.document(doc_id).get()
        return doc.to_dict()

    def get_doc_id_by_field(self, field: str, expected_value: str) -> str:
        docs = self.collection_ref.where(
            filter=FieldFilter(field, "==", expected_value)
        ).get()
        assert len(docs) == 1, "More than one document found"
        return docs[0].id

    def get_by_field(self, field: str, expected_value: str) -> T:
        docs = self.collection_ref.where(
            filter=FieldFilter(field, "==", expected_value)
        ).get()
        assert len(docs) == 1, "More than one document found"
        return docs[0].to_dict()

    def get_multiple_by_field(self, field: str, expected_value: str) -> List[T]:
        docs = self.collection_ref.where(
            filter=FieldFilter(field, "==", expected_value)
        ).get()
        return [doc.to_dict() for doc in docs]

    def get_all(self) -> List[T]:
        docs = self.collection_ref.get()
        return [doc.to_dict() for doc in docs]

    def update(self, doc_id: str, data: dict) -> str:
        self.collection_ref.document(doc_id).update(data)
        return doc_id
