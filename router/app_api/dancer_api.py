from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from config import constant
from config.common import error_response, get_current_user
from database.database import db
from database.models import User
from database.base_model import DefaultModel
from controller import dancer_controller


router = APIRouter(
    prefix='/dancer'
)


@router.get('/{dancer_id}/ticket', tags=['dancer'], summary='댄서 티켓 목록', dependencies=[Depends(get_current_user)])
def get_dancer_detail_ticket(dancer_id: int,
                             session: Session = Depends(db.session)):
    result_msg = '댄서 티켓 목록'
    try:
        response = dancer_controller.get_dancer_detail_ticket(dancer_id=dancer_id,
                                                              session=session)
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


@router.get('/lesson', tags=['dancer'], summary='댄서 수업 목록', dependencies=[Depends(get_current_user)])
def get_dancer_lesson(session: Session = Depends(db.session),
                      g: User = Depends(get_current_user)):
    result_msg = '댄서 수업 목록'
    try:
        response = dancer_controller.get_dancer_lesson(session=session,
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
