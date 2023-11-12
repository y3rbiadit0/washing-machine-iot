from fastapi import APIRouter

router = APIRouter()

@router.get("/login/")
async def root():
    return {"message": "Hello World"}