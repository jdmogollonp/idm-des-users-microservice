from fastapi import APIRouter
from api.endpoints import users, login, projects,processing

api_router = APIRouter()
api_router.include_router(login.router,prefix="/api/login", tags=["login"])
api_router.include_router(users.router, prefix="/api/users", tags=["users"])
