from fastapi import APIRouter

from utils.response import success_response

router_user = APIRouter(prefix="/api/users", tags=["users"])


@router_user.post("/login")
async def login():
    return success_response(data={"message": "Hello World!"})
