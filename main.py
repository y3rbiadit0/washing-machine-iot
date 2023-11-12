from fastapi import FastAPI

import api
import core

app = FastAPI(
    title=core.settings().app_name,
    version=core.settings().version
)
app.include_router(api.v1_router, prefix="/v1")
