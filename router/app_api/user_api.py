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
from controller import user_controller


router = APIRouter(
    prefix='/user'
)


class PostUserJoinModel(BaseModel):
    type: int = constant.USER_TYPE_MATE
    name: str
    nickname: str
    email: str
    password: str
    phone: Optional[str]
    introduction: Optional[str]


@router.post('/join', tags=['user'], summary='회원가입')
def post_user_join(request: PostUserJoinModel,
                   session: Session = Depends(db.session)):
    result_msg = '회원가입'
    try:
        response = user_controller.post_user_join(session=session,
                                                  request=request)
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


@router.get('', tags=['user'], summary='유저 목록', dependencies=[Depends(get_current_user)])
def get_user(session: Session = Depends(db.session),
             g: User = Depends(get_current_user)):
    result_msg = '유저 목록'
    try:
        response = user_controller.get_user(session=session,
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


@router.get('/{user_id}', tags=['user'], summary='유저 상세', dependencies=[Depends(get_current_user)])
def get_user_detail(user_id: int,
                    # g: User = Depends(get_current_user),
                    session: Session = Depends(db.session)):
    result_msg = '유저 상세'
    try:
        response = user_controller.get_user_detail(user_id=user_id,
                                                   # g=g,
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


@router.post('/login', tags=['user'], summary='로그인')
def post_user_login(request: OAuth2PasswordRequestForm = Depends(),
                    session: Session = Depends(db.session)):
    result_msg = '로그인'
    try:
        response = user_controller.post_user_login(session=session,
                                                   request=request)
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