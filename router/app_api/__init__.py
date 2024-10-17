from fastapi import APIRouter

from router.app_api import user_api


routers = APIRouter(
    prefix=''
)


routers.include_router(user_api.router)

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")