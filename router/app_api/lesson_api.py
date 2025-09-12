from typing import Optional, List

from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.common import error_response, get_current_user
from database.database import db
from database.models import User
from database.base_model import DefaultModel
from controller import lesson_controller


router = APIRouter(
    prefix='/lesson'
)


class PostCourseDetailModel(BaseModel):
    title: str
    course_date: str
    start_time: str
    end_time: str
    address: Optional[str]
    address_detail: Optional[str]


class PostLessonModel(BaseModel):
    status: int
    title: str
    description: str
    detail_list: List[PostCourseDetailModel]


class PostLessonDetailReviewModel(BaseModel):
    user_course_id: int
    rate: float
    description: str


@router.get('/like', tags=['lesson'], summary='수업 찜 목록', dependencies=[Depends(get_current_user)])
def get_lesson_like(session: Session = Depends(db.session),
                    g: User = Depends(get_current_user)):
    result_msg = '수업 찜 목록'
    try:
        response = lesson_controller.get_lesson_like(session=session,
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


@router.get('', tags=['lesson'], summary='수업', dependencies=[Depends(get_current_user)])
def get_lesson(session: Session = Depends(db.session),
               date: Optional[str] = None,
               g: User = Depends(get_current_user)):
    result_msg = '수업'
    try:
        response = lesson_controller.get_lesson(session=session,
                                                date=date,
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


@router.post('', tags=['lesson'], summary='수업 등록', dependencies=[Depends(get_current_user)])
def post_lesson(request: PostLessonModel,
                session: Session = Depends(db.session),
                g: User = Depends(get_current_user)):
    result_msg = '수업 등록'
    try:
        response = lesson_controller.post_lesson(request=request,
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


@router.put('/{lesson_id}', tags=['lesson'], summary='수업 수정', dependencies=[Depends(get_current_user)])
def put_lesson_detail(lesson_id: int,
                      request: PostLessonModel,
                      session: Session = Depends(db.session),
                      g: User = Depends(get_current_user)):
    result_msg = '수업 수정'
    try:
        response = lesson_controller.put_lesson_detail(lesson_id=lesson_id,
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


@router.get('/{lesson_id}', tags=['lesson'], summary='수업 상세', dependencies=[Depends(get_current_user)])
def get_lesson_detail(lesson_id: int,
                      session: Session = Depends(db.session),
                      g: User = Depends(get_current_user)):
    result_msg = '수업 상세'
    try:
        response = lesson_controller.get_lesson_detail(lesson_id=lesson_id,
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


@router.post('/{lesson_id}/like', tags=['lesson'], summary='수업 찜', dependencies=[Depends(get_current_user)])
def post_lesson_detail_like(lesson_id: int,
                            session: Session = Depends(db.session),
                            g: User = Depends(get_current_user)):
    result_msg = '수업 찜'
    try:
        response = lesson_controller.post_lesson_detail_like(lesson_id=lesson_id,
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


@router.post('/{lesson_id}/review', tags=['lesson'], summary='리뷰 작성', dependencies=[Depends(get_current_user)])
def post_lesson_detail_review(lesson_id: int,
                              request: PostLessonDetailReviewModel,
                              session: Session = Depends(db.session),
                              g: User = Depends(get_current_user)):
    result_msg = '리뷰 작성'
    try:
        response = lesson_controller.post_lesson_detail_review(lesson_id=lesson_id,
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