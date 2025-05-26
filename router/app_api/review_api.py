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
from controller import review_controller


router = APIRouter(
    prefix='/review'
)


class PutReviewDetailModel(BaseModel):
    rate: float
    description: str


@router.get('/{review_id}', tags=['review'], summary='후기 상세', dependencies=[Depends(get_current_user)])
def get_review_detail(review_id: int,
                      session: Session = Depends(db.session)):
    result_msg = '후기 상세'
    try:
        response = review_controller.get_review_detail(review_id=review_id,
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


@router.put('/{review_id}', tags=['review'], summary='후기 수정', dependencies=[Depends(get_current_user)])
def put_review_detail(review_id: int,
                      request: PutReviewDetailModel,
                      session: Session = Depends(db.session)):
    result_msg = '후기 수정'
    try:
        response = review_controller.put_review_detail(review_id=review_id,
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