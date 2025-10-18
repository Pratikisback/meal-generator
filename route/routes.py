from fastapi import APIRouter

router = APIRouter()

# You can organize routes here later, for now it's just a base router
@router.get("/ping")
def ping():
    return {"message": "pong"}