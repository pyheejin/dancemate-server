from typing import Optional, List

from PIL.ImageChops import constant
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.common import error_response, get_current_user
from database.database import db
from database.models import User
from database.base_model import DefaultModel
from controller import qna_controller


router = APIRouter(
    prefix='/qna'
)


class PostQnaModel(BaseModel):
    email: Optional[str]
    title: str
    question: str


class PostQnaAnswerModel(BaseModel):
    answer: str


@router.get('', tags=['qna'], summary='문의 목록', dependencies=[Depends(get_current_user)])
def get_qna(session: Session = Depends(db.session),
            g: User = Depends(get_current_user)):
    result_msg = '문의 목록'
    try:
        response = qna_controller.get_qna(session=session,
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


@router.post('', tags=['qna'], summary='문의 등록', dependencies=[Depends(get_current_user)])
def post_qna(request: PostQnaModel,
             session: Session = Depends(db.session),
             g: User = Depends(get_current_user)):
    result_msg = '문의 등록'
    try:
        response = qna_controller.post_qna(request=request,
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


@router.put('/{qna_id}', tags=['qna'], summary='문의 수정', dependencies=[Depends(get_current_user)])
def put_qna_detail(qna_id: int,
                   request: PostQnaModel,
                   session: Session = Depends(db.session)):
    result_msg = '문의 수정'
    try:
        response = qna_controller.put_qna_detail(qna_id=qna_id,
                                                 request=request,
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


@router.get('/{qna_id}', tags=['qna'], summary='문의 상세', dependencies=[Depends(get_current_user)])
def get_qna_detail(qna_id: int,
                   session: Session = Depends(db.session)):
    result_msg = '문의 상세'
    try:
        response = qna_controller.get_qna_detail(qna_id=qna_id,
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


@router.delete('/{qna_id}', tags=['qna'], summary='문의 삭제', dependencies=[Depends(get_current_user)])
def delete_qna_detail(qna_id: int,
                      session: Session = Depends(db.session),
                      g: User = Depends(get_current_user)):
    result_msg = '문의 삭제'
    try:
        response = qna_controller.delete_qna_detail(qna_id=qna_id,
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


@router.post('/{qna_id}/answer', tags=['qna'], summary='문의 답장', dependencies=[Depends(get_current_user)])
def post_qna_detail_answer(qna_id: int,
                           request: PostQnaAnswerModel,
                           session: Session = Depends(db.session)):
    result_msg = '문의 답장'
    try:
        response = qna_controller.post_qna_detail_answer(qna_id=qna_id,
                                                         request=request,
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