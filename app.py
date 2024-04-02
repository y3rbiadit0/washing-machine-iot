import mongomock
from fastapi import FastAPI

import api
import core
from service.mongo_service.mongo_service import MongoDBService


def create_app():
    mongodb_service = MongoDBService.init_db()
    app = FastAPI(title=core.settings().app_name, version=core.settings().version)
    app.include_router(api.v1_router, prefix="/v1")
    return app


def create_mock_app():
    mongodb_service = MongoDBService.init_db(client=mongomock.MongoClient())
    app = FastAPI(title=core.settings().app_name, version=core.settings().version)
    app.include_router(api.v1_router, prefix="/v1")
    return app
