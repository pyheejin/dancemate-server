from sqlalchemy.orm import contains_eager
from fastapi import HTTPException
from urllib3 import request

from database.models import *
from database.schema import *
from database.base_model import DefaultModel
from config.constant import *


def get_notification(session, g):
    response = DefaultModel()

    notification = session.query(Notification
                        ).outerjoin(User, User.id == Notification.user_id,
                        ).filter(Notification.user_id == g.id,
                        ).options(contains_eager(Notification.user),
                        ).first()

    if notification is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    response.result_data = {
        'notification': notification_schema.dump(notification),
    }
    return response


def post_notification(request, session, g):
    response = DefaultModel()

    notification = session.query(Notification
                        ).outerjoin(User, User.id == Notification.user_id,
                        ).filter(Notification.user_id == g.id,
                        ).options(contains_eager(Notification.user),
                        ).first()

    if notification is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    if request.lesson is not None:
        if request.lesson:
            lesson = 1
        else:
            lesson = 0
        notification.lesson = lesson

    if request.ticket is not None:
        if request.ticket:
            ticket = 1
        else:
            ticket = 0
        notification.ticket = ticket

    if request.community is not None:
        if request.community:
            community = 1
        else:
            community = 0
        notification.community = community
    return response
