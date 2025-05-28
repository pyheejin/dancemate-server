from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import constant
from config.common import error_response, get_current_user
from database.database import db
from database.models import User
from database.base_model import DefaultModel
from controller import notification_controller


router = APIRouter(
    prefix='/notification'
)


class PostNotificationModel(BaseModel):
    lesson: Optional[bool]
    ticket: Optional[bool]
    community: Optional[bool]


@router.get('', tags=['notification'], summary='알림 상세', dependencies=[Depends(get_current_user)])
def get_notification(session: Session = Depends(db.session),
                     g: User = Depends(get_current_user)):
    result_msg = '알림 상세'
    try:
        response = notification_controller.get_notification(session=session,
                                                            g=g)
    except HTTPException as e:
        print(f'error: {e.detail}')
        session.rollback()
        response = None
        response = error_response(response, e.detail, e.status_code, result_msg)
    except Exception as e:
        print(e)
        session.rollback()

        response = DefaultModel()
        response.result_msg = f'{result_msg} 실패'
        response.result_code = 210
    else:
        session.commit()
        if response is None:
            response = DefaultModel()
        if response.result_msg is not None:
            response.result_msg = f'{result_msg} 성공'
    finally:
        session.close()
    return response


@router.post('', tags=['notification'], summary='알림 수정', dependencies=[Depends(get_current_user)])
def post_notification(request: PostNotificationModel,
                      session: Session = Depends(db.session),
                      g: User = Depends(get_current_user)):
    result_msg = '알림 수정'
    try:
        response = notification_controller.post_notification(request=request,
                                                             session=session,
                                                             g=g)
    except HTTPException as e:
        print(f'error: {e.detail}')
        session.rollback()
        response = None
        response = error_response(response, e.detail, e.status_code, result_msg)
    except Exception as e:
        print(e)
        session.rollback()

        response = DefaultModel()
        response.result_msg = f'{result_msg} 실패'
        response.result_code = 210
    else:
        session.commit()
        if response is None:
            response = DefaultModel()
        if response.result_msg is not None:
            response.result_msg = f'{result_msg} 성공'
    finally:
        session.close()
    return response