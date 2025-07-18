from typing import Optional, List

from PIL.ImageChops import constant
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.common import error_response, get_current_user
from database.database import db
from database.models import User
from database.base_model import DefaultModel
from controller import course_controller


router = APIRouter(
    prefix='/course'
)


class PostCourseReserveModel(BaseModel):
    user_ticket_id: int


@router.get('/{course_id}/reserve', tags=['course'], summary='수업 예약 전', dependencies=[Depends(get_current_user)])
def get_course_detail_reserve(course_id: int,
                              session: Session = Depends(db.session),
                              g: User = Depends(get_current_user)):
    result_msg = '수업 예약 전'
    try:
        response = course_controller.get_course_detail_reserve(course_id=course_id,
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


@router.post('/{course_id}/reserve', tags=['course'], summary='수업 예약', dependencies=[Depends(get_current_user)])
def post_course_detail_reserve(course_id: int,
                               request: PostCourseReserveModel,
                               session: Session = Depends(db.session),
                               g: User = Depends(get_current_user)):
    result_msg = '수업 예약'
    try:
        response = course_controller.post_course_detail_reserve(course_id=course_id,
                                                                request=request,
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


@router.post('/{course_id}/cancel', tags=['course'], summary='수업 예약 취소', dependencies=[Depends(get_current_user)])
def post_course_detail_cancel(course_id: int,
                              session: Session = Depends(db.session),
                              g: User = Depends(get_current_user)):
    result_msg = '수업 예약 취소'
    try:
        response = course_controller.post_course_detail_cancel(course_id=course_id,
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


@router.post('/{course_id}/like', tags=['course'], summary='수업 찜', dependencies=[Depends(get_current_user)])
def post_course_detail_like(course_id: int,
                            session: Session = Depends(db.session),
                            g: User = Depends(get_current_user)):
    result_msg = '수업 찜'
    try:
        response = course_controller.post_course_detail_like(course_id=course_id,
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


@router.get('/like', tags=['course'], summary='수업 찜 목록', dependencies=[Depends(get_current_user)])
def get_course_like(session: Session = Depends(db.session),
                    g: User = Depends(get_current_user)):
    result_msg = '수업 찜 목록'
    try:
        response = course_controller.get_course_like(session=session,
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


@router.post('/{course_id}/exists', tags=['course'], summary='예약 가능 여부 확인', dependencies=[Depends(get_current_user)])
def post_course_detail_exists(course_id: int,
                              session: Session = Depends(db.session),
                              g: User = Depends(get_current_user)):
    result_msg = '예약 가능 여부 확인'
    try:
        response = course_controller.post_course_detail_exists(course_id=course_id,
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



@router.get('/{course_id}', tags=['course'], summary='수업 상세', dependencies=[Depends(get_current_user)])
def get_course_detail(course_id: int,
                      session: Session = Depends(db.session),
                      g: User = Depends(get_current_user)):
    result_msg = '수업 상세'
    try:
        response = course_controller.get_course_detail(course_id=course_id,
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

