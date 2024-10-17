from fastapi import APIRouter

from router.admin_api import user_api


routers = APIRouter(
    prefix=''
)


routers.include_router(user_api.router)