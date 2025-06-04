from fastapi import APIRouter

from router.app_api import (user_api, home_api, search_api, lesson_api,
                            payment_api, dancer_api, ticket_api, course_api,
                            review_api, notification_api, qna_api, chat_room_api,
                            calendar_api)


routers = APIRouter(
    prefix=''
)


routers.include_router(user_api.router)
routers.include_router(home_api.router)
routers.include_router(search_api.router)
routers.include_router(lesson_api.router)
routers.include_router(payment_api.router)
routers.include_router(dancer_api.router)
routers.include_router(ticket_api.router)
routers.include_router(course_api.router)
routers.include_router(review_api.router)
routers.include_router(notification_api.router)
routers.include_router(qna_api.router)
routers.include_router(chat_room_api.router)
routers.include_router(calendar_api.router)



from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')