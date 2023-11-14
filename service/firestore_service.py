from typing import TypeVar, Dict

from firebase_admin import firestore

T = TypeVar("T")


class FirestoreService:
    collection: str

    def __init__(self):
        self.db = firestore.client()
        self.collection_ref = self.db.collection(self.collection)

    def add(self, data: Dict) -> str:
        timestamp, doc_ref = self.collection_ref.add(data)
        return doc_ref.id

    def get(self, doc_id: str) -> dict:
        doc = self.collection_ref.document(doc_id).get()
        return doc.to_dict()


class ReservationFirestoreService(FirestoreService):
    collection = "reservations"

    def add(self, data: Dict) -> str:
        return super().add(data)

    def get(self, doc_id: str) -> dict:
        return super().get(doc_id)
