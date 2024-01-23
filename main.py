from fastapi import FastAPI

import api
import core
from service.mongo_service.mongo_service import MongoDBService

mongodb_service = MongoDBService.init_db()
app = FastAPI(title=core.settings().app_name, version=core.settings().version)
app.include_router(api.v1_router, prefix="/v1")
